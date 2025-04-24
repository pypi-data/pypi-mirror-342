import json
from typing import AsyncGenerator, List, Literal, Optional, Union, overload

import openai
from nonebot import logger
from openai import NOT_GIVEN
from openai.types.chat import ChatCompletionMessage, ChatCompletionToolParam

from ._types import BasicModel, Message, ModelConfig, function_call_handler
from .utils.images import get_image_base64


class Openai(BasicModel):
    def __init__(self, model_config: ModelConfig) -> None:
        super().__init__(model_config)
        self._require("api_key", "model_name")
        self.api_key = self.config.api_key
        self.model = self.config.model_name
        self.api_base = self.config.api_host if self.config.api_host else "https://api.openai.com/v1"
        self.max_tokens = self.config.max_tokens
        self.temperature = self.config.temperature
        self.stream = self.config.stream

        self.client = openai.AsyncOpenAI(api_key=self.api_key, base_url=self.api_base, timeout=30)
        self._tools: List[ChatCompletionToolParam] = []

    def __build_image_message(self, prompt: str, image_paths: List[str]) -> dict:
        user_content: List[dict] = [{"type": "text", "text": prompt}]

        for url in image_paths:
            image_format = url.split(".")[-1]
            image_url = f"data:image/{image_format};base64,{get_image_base64(local_path=url)}"
            user_content.append({"type": "image_url", "image_url": {"url": image_url}})

        return {"role": "user", "content": user_content}

    def _build_messages(
        self, prompt: str, history: List[Message], image_paths: Optional[List[str]] = [], system: Optional[str] = None
    ) -> list:
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        if history:
            for index, item in enumerate(history):
                user_content = (
                    {"role": "user", "content": item.message}
                    if not all([item.images, self.config.multimodal])
                    else self.__build_image_message(item.message, item.images)
                )

                messages.append(user_content)
                messages.append({"role": "assistant", "content": item.respond})

        user_content = (
            {"role": "user", "content": prompt} if not image_paths else self.__build_image_message(prompt, image_paths)
        )

        messages.append(user_content)

        return messages

    def _tool_call_request_precheck(self, message: ChatCompletionMessage) -> bool:
        """
        工具调用请求预检
        """
        # We expect a single tool call
        if not (message.tool_calls and len(message.tool_calls) == 1):
            return False

        # We expect the tool to be a function call
        tool_call = message.tool_calls[0]
        if tool_call.type != "function":
            return False

        return True

    async def _ask_sync(self, messages: list, **kwargs) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=False,
                tools=self._tools,
            )

            result = ""
            message = response.choices[0].message  # type:ignore
            self.total_tokens += response.usage.total_tokens if response.usage else -1

            if (
                hasattr(message, "reasoning_content")  # type:ignore
                and message.reasoning_content  # type:ignore
            ):
                result += f"<think>{message.reasoning_content}</think>"  # type:ignore

            if response.choices[0].finish_reason == "tool_calls" and self._tool_call_request_precheck(
                response.choices[0].message
            ):
                messages.append(response.choices[0].message)
                tool_call = response.choices[0].message.tool_calls[0]  # type:ignore
                arguments = json.loads(tool_call.function.arguments.replace("'", '"'))
                logger.info(f"function call 请求 {tool_call.function.name}, 参数: {arguments}")
                function_return = await function_call_handler(tool_call.function.name, arguments)
                logger.success(f"Function call 成功，返回: {function_return}")
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_call.function.name,
                        "content": function_return,
                    }
                )
                return await self._ask_sync(messages)

            if message.content:  # type:ignore
                result += message.content  # type:ignore

            return result if result else "（警告：模型无输出！）"

        except openai.APIConnectionError as e:
            error_message = f"API 连接错误: {e}"
            logger.error(error_message)
            logger.error(e.__cause__)
            self.succeed = False

        except openai.APIStatusError as e:
            error_message = f"API 状态异常: {e.status_code}({e.response})"
            logger.error(error_message)
            self.succeed = False

        return error_message

    async def _ask_stream(self, messages: list, **kwargs) -> AsyncGenerator[str, None]:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True,
                stream_options={"include_usage": True},
                tools=self._tools,
            )

            is_insert_think_label = False
            function_id = ""
            function_name = ""
            function_arguments = ""

            async for chunk in response:
                # 处理 Function call
                if chunk.usage:
                    self.total_tokens += chunk.usage.total_tokens

                if not chunk.choices:
                    continue

                if chunk.choices[0].delta.tool_calls:
                    tool_call = chunk.choices[0].delta.tool_calls[0]
                    if tool_call.id:
                        function_id = tool_call.id
                    if tool_call.function:
                        if tool_call.function.name:
                            function_name += tool_call.function.name
                        if tool_call.function.arguments:
                            function_arguments += tool_call.function.arguments

                delta = chunk.choices[0].delta
                answer_content = delta.content

                # 处理思维过程 reasoning_content
                if (
                    hasattr(delta, "reasoning_content") and delta.reasoning_content  # type:ignore
                ):
                    reasoning_content = chunk.choices[0].delta.reasoning_content  # type:ignore
                    yield (reasoning_content if is_insert_think_label else "<think>" + reasoning_content)
                    is_insert_think_label = True

                elif answer_content:
                    yield (answer_content if not is_insert_think_label else "</think>" + answer_content)
                    is_insert_think_label = False

            if function_id:
                logger.info(f"function call 请求 {function_name}, 参数: {function_arguments}")
                function_return = await function_call_handler(function_name, json.loads(function_arguments))
                logger.success(f"Function call 成功，返回: {function_return}")
                messages.append(
                    {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": function_id,
                                "type": "function",
                                "function": {"name": function_name, "arguments": function_arguments},
                            }
                        ],
                    }
                )
                messages.append(
                    {
                        "tool_call_id": function_id,
                        "role": "tool",
                        "content": function_return,
                    }
                )

                async for chunk in self._ask_stream(messages):
                    yield chunk

        except openai.APIConnectionError as e:
            error_message = f"API 连接错误: {e}"
            logger.error(error_message)
            logger.error(e.__cause__)
            yield error_message

        except openai.APIStatusError as e:
            error_message = f"API 状态异常: {e.status_code}({e.response})"
            logger.error(error_message)
            yield error_message

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
        self._tools = tools if tools else NOT_GIVEN  # type:ignore
        self.total_tokens = 0

        messages = self._build_messages(prompt, history, images, system)

        if stream:
            return self._ask_stream(messages)

        return await self._ask_sync(messages)
