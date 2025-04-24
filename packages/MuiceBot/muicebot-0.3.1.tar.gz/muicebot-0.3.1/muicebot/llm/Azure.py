import json
import os
from typing import AsyncGenerator, List, Literal, Optional, Union, overload

from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import (
    AssistantMessage,
    ChatCompletionsToolCall,
    ChatCompletionsToolDefinition,
    ChatRequestMessage,
    CompletionsFinishReason,
    ContentItem,
    FunctionCall,
    FunctionDefinition,
    ImageContentItem,
    ImageDetailLevel,
    ImageUrl,
    SystemMessage,
    TextContentItem,
    ToolMessage,
    UserMessage,
)
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from nonebot import logger

from ._types import BasicModel, Message, ModelConfig, function_call_handler


class Azure(BasicModel):
    def __init__(self, model_config: ModelConfig) -> None:
        super().__init__(model_config)
        self._require("model_name")
        self.model_name = self.config.model_name
        self.max_tokens = self.config.max_tokens
        self.temperature = self.config.temperature
        self.top_p = self.config.top_p
        self.frequency_penalty = self.config.frequency_penalty
        self.presence_penalty = self.config.presence_penalty
        self.token = os.getenv("AZURE_API_KEY", self.config.api_key)
        self.endpoint = self.config.api_host if self.config.api_host else "https://models.inference.ai.azure.com"

        self._tools: List[ChatCompletionsToolDefinition] = []

    def __build_image_messages(self, prompt: str, image_paths: list) -> UserMessage:
        image_content_items: List[ContentItem] = []

        for item in image_paths:
            image_content_items.append(
                ImageContentItem(
                    image_url=ImageUrl.load(
                        image_file=item, image_format=item.split(".")[-1], detail=ImageDetailLevel.AUTO
                    )
                )
            )

        content = [TextContentItem(text=prompt)] + image_content_items

        return UserMessage(content=content)

    def __build_tools_definition(self, tools: List[dict]) -> List[ChatCompletionsToolDefinition]:
        tool_definitions = []

        for tool in tools:
            tool_definition = ChatCompletionsToolDefinition(
                function=FunctionDefinition(
                    name=tool["function"]["name"],
                    description=tool["function"]["description"],
                    parameters=tool["function"]["parameters"],
                )
            )
            tool_definitions.append(tool_definition)

        return tool_definitions

    def _build_messages(
        self, prompt: str, history: List[Message], image_paths: Optional[List] = None, system: Optional[str] = None
    ) -> List[ChatRequestMessage]:
        messages: List[ChatRequestMessage] = []

        if system:
            messages.append(SystemMessage(system))

        for msg in history:
            user_msg = (
                UserMessage(msg.message)
                if not msg.images
                else self.__build_image_messages(msg.message, image_paths=msg.images)
            )
            messages.append(user_msg)
            messages.append(AssistantMessage(msg.respond))

        user_message = UserMessage(prompt) if not image_paths else self.__build_image_messages(prompt, image_paths)

        messages.append(user_message)

        return messages

    def _tool_messages_precheck(self, tool_calls: Optional[List[ChatCompletionsToolCall]] = None) -> bool:
        if not (tool_calls and len(tool_calls) == 1):
            return False

        tool_call = tool_calls[0]

        if isinstance(tool_call, ChatCompletionsToolCall):
            return True

        return False

    async def _ask_sync(self, messages: List[ChatRequestMessage]) -> str:
        client = ChatCompletionsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.token))

        try:
            response = await client.complete(
                messages=messages,
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                stream=False,
                tools=self._tools,
            )
            finish_reason = response.choices[0].finish_reason
            self.total_tokens += response.usage.total_tokens

            if finish_reason == CompletionsFinishReason.STOPPED:
                return response.choices[0].message.content  # type: ignore

            elif finish_reason == CompletionsFinishReason.CONTENT_FILTERED:
                self.succeed = False
                return "(模型内部错误: 被内容过滤器阻止)"

            elif finish_reason == CompletionsFinishReason.TOKEN_LIMIT_REACHED:
                self.succeed = False
                return "(模型内部错误: 达到了最大 token 限制)"

            elif finish_reason == CompletionsFinishReason.TOOL_CALLS:
                tool_calls = response.choices[0].message.tool_calls
                messages.append(AssistantMessage(tool_calls=tool_calls))
                if not self._tool_messages_precheck(tool_calls=tool_calls):
                    self.succeed = False
                    return "(模型内部错误: tool_calls 内容为空)"

                tool_call = tool_calls[0]  # type:ignore
                function_args = json.loads(tool_call.function.arguments.replace("'", '"'))
                logger.info(f"function call 请求 {tool_call.function.name}, 参数: {function_args}")
                function_return = await function_call_handler(tool_call.function.name, function_args)
                logger.success(f"Function call 成功，返回: {function_return}")

                # Append the function call result fo the chat history
                messages.append(ToolMessage(tool_call_id=tool_call.id, content=function_return))

                return await self._ask_sync(messages)

            return "(模型内部错误: 未知错误)"

        except HttpResponseError as e:
            logger.error(f"模型响应失败: {e.status_code} ({e.reason})")
            logger.error(f"{e.message}")
            self.succeed = False
            return f"模型响应失败: {e.status_code} ({e.reason})"
        finally:
            await client.close()

    async def _ask_stream(self, messages: List[ChatRequestMessage]) -> AsyncGenerator[str, None]:
        client = ChatCompletionsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.token))

        try:
            response = await client.complete(
                messages=messages,
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                stream=True,
                tools=self._tools,
                model_extras={"stream_options": {"include_usage": True}},  # 需要显式声明获取用量
            )

            tool_call_id: str = ""
            function_name: str = ""
            function_args: str = ""

            async for chunk in response:
                if chunk:  # chunk.usage 只会在最后一个包中被提供，此时choices为空
                    self.total_tokens += chunk.usage.total_tokens if chunk.usage else 0

                if not chunk.choices:
                    continue

                finish_reason = chunk.choices[0].finish_reason

                if chunk.choices and chunk.choices[0].get("delta", {}).get("content", ""):
                    yield chunk["choices"][0]["delta"]["content"]
                    continue

                elif chunk.choices[0].delta.tool_calls is not None:
                    tool_call = chunk.choices[0].delta.tool_calls[0]

                    if tool_call.function.name is not None:
                        function_name = tool_call.function.name
                    if tool_call.id is not None:
                        tool_call_id = tool_call.id
                    function_args += tool_call.function.arguments or ""
                    continue

                elif finish_reason == CompletionsFinishReason.CONTENT_FILTERED:
                    self.succeed = False
                    yield "(模型内部错误: 被内容过滤器阻止)"

                elif finish_reason == CompletionsFinishReason.TOKEN_LIMIT_REACHED:
                    self.succeed = False
                    yield "(模型内部错误: 达到了最大 token 限制)"

                elif finish_reason == CompletionsFinishReason.TOOL_CALLS:
                    messages.append(
                        AssistantMessage(
                            tool_calls=[
                                ChatCompletionsToolCall(
                                    id=tool_call_id, function=FunctionCall(name=function_name, arguments=function_args)
                                )
                            ]
                        )
                    )

                    function_arg = json.loads(function_args.replace("'", '"'))
                    logger.info(f"function call 请求 {function_name}, 参数: {function_arg}")
                    function_return = await function_call_handler(function_name, function_arg)
                    logger.success(f"Function call 成功，返回: {function_return}")

                    # Append the function call result fo the chat history
                    messages.append(ToolMessage(tool_call_id=tool_call_id, content=function_return))

                    async for content in self._ask_stream(messages):
                        yield content

                    return

        except HttpResponseError as e:
            logger.error(f"模型响应失败: {e.status_code} ({e.reason})")
            logger.error(f"{e.message}")
            yield f"模型响应失败: {e.status_code} ({e.reason})"
            self.succeed = False
        finally:
            await client.close()

    @overload
    async def ask(
        self,
        prompt: str,
        history: List[Message],
        images: Optional[List[str]] = [],
        tools: Optional[List[dict]] = [],
        stream: Literal[False] = False,
        system: Optional[str] = None,
        **kwargs,
    ) -> str: ...

    @overload
    async def ask(
        self,
        prompt: str,
        history: List[Message],
        images: Optional[List[str]] = [],
        tools: Optional[List[dict]] = [],
        stream: Literal[True] = True,
        system: Optional[str] = None,
        **kwargs,
    ) -> AsyncGenerator[str, None]: ...

    async def ask(
        self,
        prompt: str,
        history: List[Message],
        images: Optional[List[str]] = [],
        tools: Optional[List[dict]] = [],
        stream: Optional[bool] = False,
        system: Optional[str] = None,
        **kwargs,
    ) -> Union[AsyncGenerator[str, None], str]:
        self.succeed = True
        self.total_tokens = 0

        messages = self._build_messages(prompt, history, images, system)

        self._tools = self.__build_tools_definition(tools) if tools else []

        if stream:
            return self._ask_stream(messages)

        return await self._ask_sync(messages)
