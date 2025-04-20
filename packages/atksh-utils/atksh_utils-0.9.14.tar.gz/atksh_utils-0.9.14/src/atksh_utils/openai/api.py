import copy
import io
import json
import math
import multiprocessing as mp
import os
import traceback
from concurrent.futures import ThreadPoolExecutor as TPE
from datetime import datetime
from functools import partial
from typing import Optional, Tuple, TypedDict, Union

import backoff
import numpy as np
import openai
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionContentPartImageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_chunk import ChoiceDelta, ChoiceDeltaToolCall
from openai.types.chat.chat_completion_content_part_image_param import ImageURL
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)

from ..nlp.str_kernel import build_kernel
from .functional import FunctionWrapper, function_info
from .prompt import generate_prompt
from .token import count_token
from .tool import (
    append_to_file,
    get_browser_functions,
    get_run_subtask_function,
    local_python_executor,
    parse_args,
    python_package_installer,
    read_file,
    reset_python_session,
    shell_command_executor,
    write_file,
)

ChatCompletionMessageType = Union[
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionMessage,
]


def verbose():
    return os.getenv("ASKGPT_VERBOSE", "0") == "1"


class OpenAI:
    """
    A class for interacting with the OpenAI API.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        oai=None,
        *,
        max_num_messages: int = 10000,
        max_num_input_tokens: int = -1,
        is_child=False,
    ) -> None:
        """
        Initializes the OpenAI class.

        Args:
            api_key (str): The API key for accessing the OpenAI API.
            model_name (str): The name of the OpenAI model to use.
            temperature (float): The temperature to use for the OpenAI API. Defaults to 0.7.
            top_p (float): The top_p to use for the OpenAI API. Defaults to 0.9.
            oai (Any): The OpenAI module to use. If None, the module will be imported.
            max_num_messages (int): The maximum number of messages to keep in the chat history. Defaults to 48.
            max_num_input_tokens (int): The maximum number of tokens to use for the user prompt. Defaults to 16000.
            is_child (bool): Whether the OpenAI instance is a child of another OpenAI instance. Defaults to False.
        """
        self.api_key = api_key
        self.openai = oai if oai is not None else openai
        self.openai.api_key = self.api_key
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self._functions: list[FunctionWrapper] = []
        self.max_num_messages = max_num_messages
        if max_num_input_tokens > 0:
            self.max_num_input_tokens = max_num_input_tokens
        elif "gpt-4.1" in self.model_name:
            # GPT-4.1 supports up to 1M tokens
            self.max_num_input_tokens = 1000000
        elif "gpt-4-0125-preview" in self.model_name or "gpt-4o" in self.model_name:
            # GPT-4o and earlier preview models support up to 120K tokens
            self.max_num_input_tokens = 120000
        elif "gpt-4-32k-0613" in self.model_name:
            # 32K variant
            self.max_num_input_tokens = 28000
        else:
            self.max_num_input_tokens = 15000
        self.is_child = is_child

        self.prev_total_tokens = 0

        self.messages_to_save_num = 2
        self.system_prompt = (
            generate_prompt() + f"\nCurrent date and time: {datetime.now().isoformat()}"
        )
        reset_python_session()

    @property
    def tools(self) -> list[ChatCompletionToolParam]:
        return [f.as_tool() for f in self._functions]

    @property
    def func_names(self) -> list[str]:
        return [f.info["name"] for f in self._functions]

    def speech(self, text: str) -> None:
        try:
            import sounddevice as sd
            import soundfile as sf
        except:
            e = traceback.format_exc()
            print("Failed to import sounddevice and soundfile.\n")
            print(e)
            return
        texts = []
        while len(text) > 2048:
            # split at the end of the sentence.
            # end of the sentence is defined as the last period in the text or \n or 。 or ．
            idx = max(
                text[:3096].rfind("."),
                text[:3096].rfind("\n"),
                text[:3096].rfind("。"),
                text[:3096].rfind("．"),
            )
            if idx == -1:
                idx = text[:3096].rfind(" ")
            if idx == -1:
                idx = 3096
            texts.append(text[:idx])
            text = text[idx:]
        texts.append(text)  # append the remaining text
        for text in texts:
            spoken_response = self.openai.audio.speech.create(
                model="tts-1-hd",
                voice="fable",
                response_format="opus",
                input=text,
            )
            with io.BytesIO() as buffer:
                buffer.write(spoken_response.content)
                buffer.seek(0)
                with sf.SoundFile(buffer, "r") as sound_file:
                    data = sound_file.read(dtype="int16")
                    sd.play(data, sound_file.samplerate)
                    sd.wait()

    def make_child(self, model_name=None, temperature=None, top_p=None, *, use_func=False):
        child = OpenAI(
            self.api_key,
            self.model_name if model_name is None else model_name,
            self.temperature if temperature is None else temperature,
            self.top_p if top_p is None else top_p,
            self.openai,
            is_child=True,
        )
        if use_func:
            child._functions = self._functions
        return child

    def set_function(self, func):
        """
        Adds a function to the list of functions that can be called by the OpenAI API.

        Args:
            func: The function to add.
        """
        self._functions.append(function_info(func))

    def add_instructions(self, instructions: Union[str, list[str]]):
        """
        Adds instructions to the system prompt.

        Args:
            prompt (str): The system prompt to set.
        """
        if isinstance(instructions, str):
            instructions = [instructions]
        instructions = list(map(lambda x: x.replace("\n", " ").strip(), instructions))
        more = "•" + "\n•".join(instructions) + "\n"
        self.system_prompt = generate_prompt(more)

    def set_system_prompt(self, prompt: str):
        """
        Sets the system prompt.

        Args:
            prompt (str): The system prompt to set.
        """
        self.system_prompt = prompt

    def step(self, deltas: list[ChoiceDelta]) -> ChatCompletionMessage:
        role = None
        content = None

        index_to_id: dict[int, str] = dict()
        id_to_name: dict[str, str] = dict()
        id_to_args: dict[str, str] = dict()

        for delta in deltas:
            if delta.role is not None and role is None:
                role = delta.role
            if delta.role == "assistant" and content is None:
                content = delta.content
            elif delta.content is not None:
                content += delta.content

            if delta.tool_calls:
                tool_call: ChoiceDeltaToolCall
                for tool_call in delta.tool_calls:
                    if tool_call.type == "function":
                        if tool_call.index is not None and tool_call.id is not None:
                            index_to_id[tool_call.index] = tool_call.id
                            id_to_name[tool_call.id] = tool_call.function.name
                            id_to_args[tool_call.id] = tool_call.function.arguments
                        else:
                            raise ValueError(f"Invalid tool call: {tool_call}")
                    else:
                        if (call_id := index_to_id.get(tool_call.index)) is not None:
                            id_to_args[call_id] += tool_call.function.arguments

        tool_calls: list[ChatCompletionMessageToolCall] = []
        for tc_id in index_to_id.values():
            func: Function = Function(arguments=id_to_args[tc_id], name=id_to_name[tc_id])
            tool_call = ChatCompletionMessageToolCall(
                id=tc_id,
                function=func,
                type="function",
            )
            tool_calls.append(tool_call)
        if len(tool_calls) > 0:
            return ChatCompletionMessage(role=role, content=content, tool_calls=tool_calls)
        else:
            return ChatCompletionMessage(role=role, content=content)

    def _create_message_param(
        self, role: str, content: str, tool_call_id: str | None = None
    ) -> Union[
        ChatCompletionSystemMessageParam,
        ChatCompletionUserMessageParam,
        ChatCompletionAssistantMessageParam,
        ChatCompletionToolMessageParam,
    ]:
        if role == "system":
            return ChatCompletionSystemMessageParam({"role": role, "content": content})
        elif role == "user":
            assert tool_call_id is None
            return ChatCompletionUserMessageParam({"role": role, "content": content})
        elif role == "assistant":
            assert tool_call_id is None
            return ChatCompletionAssistantMessageParam({"role": role, "content": content})
        elif role == "system":
            assert tool_call_id is None
            return ChatCompletionSystemMessageParam({"role": role, "content": content})
        elif role == "tool":
            return ChatCompletionToolMessageParam(
                {"role": role, "content": content, "tool_call_id": tool_call_id}
            )
        else:
            raise ValueError(f"Invalid role: {role}")

    @staticmethod
    def _is_chat_completion_message_type(message: Union[dict, ChatCompletionMessageType]) -> bool:
        if isinstance(message, dict):
            return False
        if isinstance(message, ChatCompletionMessage):
            return True
        raise ValueError(f"Invalid message type: {message}")

    def is_last_message_assistant(self, messages: list[Union[dict, ChatCompletionMessage]]) -> bool:
        raise NotImplementedError("This function is not implemented yet.")
        if len(messages) == 0:
            return False
        last_message = messages[-1]
        if (
            getattr(last_message, "role", None) == "assistant"
            and getattr(last_message, "tool_calls", None) is None
        ):
            return True
        return False

    def is_last_message_tool_call(self, messages: list[Union[dict, ChatCompletionMessage]]) -> bool:
        raise NotImplementedError("This function is not implemented yet.")
        if len(messages) == 0:
            return False
        last_message = messages[-1]
        if not isinstance(last_message, dict):
            return False
        if last_message["role"] == "tool":
            return True
        return False

    def _clean_tool_calls_after_assistant_answer(
        self,
        messages: list[Union[dict, ChatCompletionMessage]],
    ) -> list[Union[dict, ChatCompletionMessage]]:
        raise NotImplementedError("This function is not implemented yet.")
        if messages is None or len(messages) <= 2:
            return messages
        for i in range(len(messages), self.messages_to_save_num, -1):
            if self.is_last_message_tool_call(messages[: i - 1]) and self.is_last_message_assistant(
                messages[:i]
            ):
                messages = self._del_message_by_index(messages, i - 2, replace_tool_call=True)
                return self._clean_tool_calls_after_assistant_answer(messages)
        return messages

    def _del_message_by_index_mask(
        self,
        messages: list[Union[dict, ChatCompletionMessage]],
        index: int,
        *,
        mask: Optional[list[bool]] = None,
    ):
        if mask is None:
            mask = [True for _ in range(len(messages))]
        mask[index] = False
        assert all(isinstance(m, bool) for m in mask)

        target = messages[index]
        if isinstance(target, dict) and (
            (tool_call_id := target.get("tool_call_id", None)) is not None
        ):
            # If the target is a tool call, delete the caller message and the callees
            for i, message in enumerate(messages[:index]):
                if (
                    isinstance(message, ChatCompletionMessage)
                    and (tool_calls := message.tool_calls) is not None
                ):
                    # If the caller message has the same tool call, delete the caller message
                    if mask[i] and any([tool_call.id == tool_call_id for tool_call in tool_calls]):
                        mask = self._del_message_by_index_mask(messages, i, mask=mask)
        elif (
            isinstance(target, ChatCompletionMessage)
            and ((tool_calls := target.tool_calls) is not None)
            and index + 1 < len(messages)
        ):
            # If the target is a message with tool calls, delete the callees
            for tool_call in tool_calls:
                for j in range(index + 1, len(messages)):
                    if (
                        mask[j]
                        and isinstance(messages[j], dict)
                        and messages[j].get("tool_call_id") == tool_call.id
                    ):
                        mask = self._del_message_by_index_mask(messages, j, mask=mask)

        return mask

    def _del_message_by_index(
        self,
        messages: list[Union[dict, ChatCompletionMessage]],
        index: int,
        *,
        mask: Optional[list[bool]] = None,
        replace_tool_call: bool = False,
    ):
        assert all(isinstance(m, (dict, ChatCompletionMessage)) for m in messages)
        if mask is not None:
            assert all(isinstance(m, bool) for m in mask)
            assert len(mask) == len(messages)
        mask = self._del_message_by_index_mask(messages, index, mask=mask)
        assert len(mask) == len(messages)
        if replace_tool_call:
            new_messages = []
            for m, msk in zip(messages, mask):
                if msk:
                    new_messages.append(m)
                elif isinstance(m, dict) and "tool_call_id" in m:
                    pass
                elif isinstance(m, ChatCompletionMessage) and m.tool_calls is not None:
                    if m.content is not None:
                        m.tool_calls = None
                        new_messages.append(m)
                else:
                    pass
            return new_messages
        return [message for message, m in zip(messages, mask) if m]

    @backoff.on_exception(
        partial(backoff.expo, base=3, factor=4),
        (openai.APIError, openai.RateLimitError),
        jitter=backoff.full_jitter,
        max_tries=5,
        max_time=120,
    )
    def call(
        self,
        user_prompt: Optional[str] = None,
        messages: Optional[list[ChatCompletionMessage]] = None,
        stream_callback=None,
    ) -> list[ChatCompletionMessage]:
        """
        Calls the OpenAI API with the given user prompt and messages.

        Args:
            user_prompt (Optional[str]): The user prompt to use. Defaults to None.
            messages (Optional[list[ChatCompletionMessage]]): The messages to use. Defaults to None.
            stream_callback (Optional[Callable[[Dict[str, str]], None]]): A callback function to call for each message returned by the OpenAI API. Defaults to None.

        Returns:
            list[ChatCompletionMessage]: The messages returned by the OpenAI API.
        """
        if messages is None:
            messages = []
            messages.append(self._create_message_param("system", self.system_prompt))
            assert user_prompt is not None, "user_prompt is required when messages is None"
            messages.append(self._create_message_param("user", user_prompt))
        elif isinstance(user_prompt, str) and len(user_prompt) > 0:
            messages.append(self._create_message_param("user", user_prompt))
        messages = self.truncate(messages)

        try:
            if len(self.tools) > 0:
                response = self.openai.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    stream=stream_callback is not None,
                    tools=self.tools,
                    tool_choice="auto",
                    max_tokens=16384,
                )
            else:
                response = self.openai.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    stream=stream_callback is not None,
                    max_tokens=16384,
                )
        except Exception as e:
            traceback.print_exc()
            raise e

        total_tokens = self.prev_total_tokens
        message: ChatCompletionMessage
        if stream_callback is not None:
            deltas = []
            for chunk in response:
                delta = chunk.choices[0].delta
                deltas.append(delta)
                stream_callback(chunk, self.step(deltas))
                if "usage" in chunk and "total_tokens" in chunk["usage"]:
                    total_tokens = chunk["usage"]["total_tokens"]
                else:
                    total_tokens += 1
            message = self.step(deltas)
        else:
            message = response.choices[0].message
            total_tokens = response.usage.total_tokens
        messages.append(message)
        self.prev_total_tokens = total_tokens

        if (tool_calls := message.tool_calls) is not None:
            tool_response_messages = []
            with TPE(max_workers=mp.cpu_count()) as exe:
                futures = []
                tool_call: ChatCompletionMessageToolCall
                for tool_call in tool_calls:
                    if tool_call.type == "function":
                        function = tool_call.function
                        function_name = function.name
                        msg = None
                        try:
                            func = self._functions[self.func_names.index(function_name)]
                        except:
                            function_names = [function_name]
                            function_names.extend([func.info["name"] for func in self._functions])
                            dist = build_kernel(function_names, n=4, lam=0.8)[0, 1:]
                            idx = dist.argmin()
                            func = self._functions[idx]
                            msg = f"Unknown function: {function_name}. Did you mean {func.info['name']}?\n"

                        if msg is None:
                            filtered_args = {}
                            original_args = repr(function.arguments)
                            function_call_args = parse_args(function.arguments)
                            if isinstance(function_call_args, str):
                                if msg is None:
                                    msg = ""
                                msg += f"The arguments of {function_name} is invalid: {function_call_args}.\n"
                                msg += f"Please check the arguments: {json.dumps(func.info['parameters']['properties'],  ensure_ascii=False)}.\n"
                                futures.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "role": "tool",
                                        "content": msg,
                                        "args": original_args,
                                    }
                                )
                            else:
                                for arg, value in function_call_args.items():
                                    if arg in func.info["parameters"]["properties"]:
                                        filtered_args[arg] = value
                                future = exe.submit(func, **filtered_args)
                                futures.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "role": "tool",
                                        "content": future,
                                        "args": original_args,
                                    }
                                )
                        else:
                            futures.append(
                                {
                                    "tool_call_id": tool_call.id,
                                    "role": "tool",
                                    "content": msg,
                                    "args": None,
                                }
                            )
                    else:
                        raise NotImplementedError(f"Unknown tool call type: {tool_call.type}")
                for future in futures:
                    content = future["content"]
                    if not isinstance(content, str):
                        if (error := content.exception()) is not None:
                            if verbose():
                                print(f"\033[0m\033[91m{error}\033[0m")
                            content = f"Error: {str(error)}\n"
                            content += f"The argment was {future['args']}"
                        else:
                            content = content.result()
                    future["content"] = json.dumps(content, ensure_ascii=False)
                    del future["args"]
                    tool_response_messages.append(self._create_message_param(**future))
                messages.extend(tool_response_messages)

            messages = self.truncate(messages, disable_verbose=True)
            return self.call(None, messages, stream_callback=stream_callback)

        return self.truncate(messages)

    @staticmethod
    def count_token(messages: list[ChatCompletionMessage]) -> list[int]:
        tokens_per_message = []
        for message in messages:
            if isinstance(message, ChatCompletionMessage):
                content = message.content
                if content is None:
                    content = ""
                tmp = count_token(content)
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        tmp += count_token(tool_call.function.arguments)
                        tmp += count_token(tool_call.function.name)
                        tmp += count_token(tool_call.id)
                        tmp += count_token(tool_call.type)
                tokens_per_message.append(tmp)
            else:
                tokens_per_message.append(count_token(message["content"]))
        return tokens_per_message

    def truncate(
        self, messages: list[ChatCompletionMessage], disable_verbose: bool = False
    ) -> list[ChatCompletionMessage]:
        """
        Truncates the messages to the maximum number of messages.

        Args:
            messages (list[ChatCompletionMessage]): The messages to truncate.
            disable_verbose (bool): Whether to disable verbose mode. Defaults to False.

        Returns:
            list[ChatCompletionMessage]: The truncated messages.
        """
        if not messages or (len(messages) <= self.messages_to_save_num + 1):
            return messages
        while len(messages) > self.max_num_messages:
            if verbose() and not self.is_child:
                print(f"Truncate: {len(messages)}")
            messages = self._del_message_by_index(messages, self.messages_to_save_num)
        tokens_per_message = np.array(self.count_token(messages))
        prefix_token_count = tokens_per_message[: self.messages_to_save_num].sum()
        tokens_per_message = tokens_per_message[self.messages_to_save_num :].copy()
        tokens_per_message[0] += prefix_token_count

        reversed_cumsum = tokens_per_message[::-1].cumsum()[::-1]
        n_to_remove = math.ceil(np.sum(reversed_cumsum > self.max_num_input_tokens))
        n_messages = len(messages)
        if verbose() and not self.is_child and not disable_verbose:
            print(
                f"n_to_remove: {n_to_remove}/{len(messages) - self.messages_to_save_num}",
                reversed_cumsum,
            )
        for _ in range(n_to_remove):
            if len(messages) <= self.messages_to_save_num:
                break
            messages = self._del_message_by_index(messages, self.messages_to_save_num)
        if n_to_remove > 0:
            assert (
                len(messages) <= n_messages - n_to_remove
            ), f"Truncated messages length: {len(messages)} != {n_messages - n_to_remove}"
        else:
            assert (
                len(messages) == n_messages
            ), f"Truncated messages length: {len(messages)} != {n_messages}"
        return messages

    def try_call(
        self,
        user_prompt: str,
        messages: Optional[list[ChatCompletionMessage]] = None,
        stream_callback=None,
    ):
        try:
            messages = self.call(
                user_prompt,
                messages,
                stream_callback=stream_callback,
            )
        except Exception as e:
            traceback.print_exc()
            raise e
        return messages

    def __call__(
        self,
        user_prompt: str,
        stream_callback=None,
    ) -> Tuple[list[ChatCompletionMessage], str]:
        """
        Calls the OpenAI API with the given user prompt.

        Args:
            user_prompt (str): The user prompt to use.

        Returns:
            Tuple[list[ChatCompletionMessage], str]: The messages returned by the OpenAI API and the final response.
        """
        messages = self.try_call(
            user_prompt,
            stream_callback=stream_callback,
        )
        return messages, messages[-1].content

    def __repr__(self) -> str:
        return f"OpenAI(model_name={self.model_name}, temperature={self.temperature}, top_p={self.top_p})"

    def set_browser_functions(self):
        web_search, extract_page_content_from_url, extract_content_from_file = (
            get_browser_functions(self)
        )
        self.set_function(web_search)
        self.set_function(extract_page_content_from_url)
        self.set_function(extract_content_from_file)

    def set_python_functions(self):
        self.set_function(local_python_executor)
        self.set_function(python_package_installer)
        self.set_function(reset_python_session)

    def set_bash_function(self):
        self.set_function(shell_command_executor)
        self.set_function(write_file)
        self.set_function(read_file)
        self.set_function(append_to_file)

    def set_utility_functions(self):
        self.set_function(get_run_subtask_function(self))
