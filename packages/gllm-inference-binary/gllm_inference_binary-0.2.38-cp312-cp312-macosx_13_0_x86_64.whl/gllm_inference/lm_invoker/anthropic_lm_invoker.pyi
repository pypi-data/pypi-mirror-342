from _typeshed import Incomplete
from enum import StrEnum
from gllm_core.event import EventEmitter as EventEmitter
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from gllm_inference.schema import LMOutput as LMOutput, MimeType as MimeType, MultimodalContent as MultimodalContent, MultimodalOutput as MultimodalOutput, MultimodalPrompt as MultimodalPrompt, PromptRole as PromptRole, Reasoning as Reasoning, ToolCall as ToolCall, ToolResult as ToolResult
from gllm_inference.utils import get_mime_type as get_mime_type, is_local_file_path as is_local_file_path, is_remote_file_path as is_remote_file_path
from langchain_core.tools import Tool as Tool
from pydantic import BaseModel as BaseModel
from typing import Any

VALID_EXTENSIONS_MAP: Incomplete
DEFAULT_MAX_TOKENS: int
DEFAULT_THINKING_BUDGET: int

class _Key(StrEnum):
    """Defines valid keys in Anthropic."""
    CONTENT = 'content'
    DATA = 'data'
    ID = 'id'
    INPUT = 'input'
    MEDIA_TYPE = 'media_type'
    NAME = 'name'
    SIGNATURE = 'signature'
    SOURCE = 'source'
    THINKING = 'thinking'
    TOOL_USE_ID = 'tool_use_id'
    TEXT = 'text'
    TYPE = 'type'

class _InputType(StrEnum):
    """Defines valid input types in Anthropic."""
    IMAGE = 'image'
    REDACTED_THINKING = 'redacted_thinking'
    TEXT = 'text'
    THINKING = 'thinking'
    TOOL_RESULT = 'tool_result'
    TOOL_USE = 'tool_use'

class _OutputType(StrEnum):
    """Defines valid output types in Anthropic."""
    CONTENT_BLOCK_DELTA = 'content_block_delta'
    CONTENT_BLOCK_STOP = 'content_block_stop'
    REDACTED_THINKING = 'redacted_thinking'
    TEXT = 'text'
    TEXT_DELTA = 'text_delta'
    THINKING = 'thinking'
    THINKING_DELTA = 'thinking_delta'
    TOOL_USE = 'tool_use'

class AnthropicLMInvoker(BaseLMInvoker):
    '''A language model invoker to interact with Anthropic language models.

    Attributes:
        client (AsyncAnthropic): The Anthropic client instance.
        model_name (str): The name of the Anthropic language model.
        default_hyperparameters (dict[str, Any]): Default hyperparameters for invoking the model.
        valid_extensions_map (dict[str, set[str]]): A dictionary mapping for validating the content type of the
            multimodal inputs. The keys are the mime types (e.g. "image") and the values are the set of valid
            file extensions (e.g. {".png", ".jpg", ".jpeg"}) for the corresponding mime type.
        valid_extensions (set[str]): A set of valid file extensions for the multimodal inputs.
        tools (list[Tool]): Tools provided to the language model to enable tool calling.
        response_schema (BaseModel | None): The schema of the response. If provided, a structured output in the form
            of a Pydantic model will be included in the output.
        use_thinking (bool): Whether to enable thinking.
        thinking_budget (int): The tokens allocated for the thinking process. Ignored if `use_thinking = False`.
        output_thinking (bool): Whether to output the thinking token. Ignored if `use_thinking = False`.

    Supported input types:
        The `AnthropicLMInvoker` supports the following input types:
        1. Text.
        2. Image: ".jpg", ".jpeg", ".png", ".gif", and ".webp".

        Non-text inputs must be of valid file extensions and can be passed as either:
        1. Base64 encoded bytes.
        2. Remote URLs, with a valid `http` or `https` scheme.
        3. Existing local file paths.

        Usage example:
        ```python
        text = "What animal is in this image?"
        image = "path/to/local/image.png"

        prompt = [(PromptRole.USER, [text, image])]
        result = await lm_invoker.invoke(prompt)
        ```

    Tool calling:
        Tool calling is a feature that allows the language model to call tools to perform tasks.
        Tools can be passed to the via the `tools` parameter as a list of LangChain\'s `Tool` objects.
        When tools are provided and the model decides to call a tool, the tool calls are stored in the
        `tool_calls` attribute in the output.

        Usage example:
        ```python
        lm_invoker = AnthropicLMInvoker(..., tools=[tool_1, tool_2])
        ```

        Output example:
        ```python
        LMOutput(
            response="Let me call the tools...",
            tool_calls=[
                ToolCall(id="123", name="tool_1", args={"key": "value"}),
                ToolCall(id="456", name="tool_2", args={"key": "value"}),
            ]
        )
        ```

    Structured output:
        Structured output is a feature that allows the language model to output a structured response in the form of a
        Pydantic model. This feature can be enabled by providing a Pydantic model to the `response_schema` parameter.
        When enabled, the structured output is stored in the `structured_output` attribute in the output.

        Usage example:
        ```python
        class Animal(BaseModel):
            name: str
            color: str

        lm_invoker = AnthropicLMInvoker(..., response_schema=Animal)
        ```

        Output example:
        ```python
        LMOutput(
            response="",
            structured_output=Animal(name="Golden retriever", color="Golden"),
        )
        ```

        The structured output is achieved by providing the schema name in the `tool_choice` parameter. This forces
        the model to call the provided schema as a tool. The tool call arguments are then validated against the schema
        and returned as a Pydantic model.

        Thus, structured output is not compatible with:
        1. Tool calling, since the tool calling is reserved to force the model to call the provided schema as a tool.
        2. Thinking, since thinking is not allowed when a tool use is forced through the `tool_choice` parameter.

        The language model also doesn\'t need to stream anything when structured output is enabled. Thus, standard
        invocation will be performed regardless of whether the `event_emitter` parameter is provided or not.

    Thinking:
        Thinking is a feature that allows the language model to have enhanced reasoning capabilities for complex tasks,
        while also providing transparency into its step-by-step thought process before it delivers its final answer.
        This feature is only available for certain models (As of March 2025, only Claude 3.7 Sonnet) and can be enabled
        by setting the `use_thinking` parameter to `True`.

        When thinking is enabled, the amount of tokens allocated for the thinking process can be set via the
        `thinking_budget` parameter. The `thinking_budget`:
        1. Must be greater than or equal to 1024.
        2. Must be less than the `max_tokens` hyperparameter, as the `thinking_budget` is allocated from the
           `max_tokens`. For example, if `max_tokens=2048` and `thinking_budget=1024`, the language model will
           allocate at most 1024 tokens for thinking and the remaining 1024 tokens for generating the response.

        When thinking is enabled, the output can also be configured either to output the thinking or not along with
        the response via the `output_thinking` parameter:
        1. Standard mode with `output_thinking = False`
            Return a string containing the response.
            Output example:
            ```python
            "Golden retriever is a good dog breed."
            ```
        2. Standard mode with `output_thinking = True`
            Return an `LMOutput` object that contains a `reasoning` attributes with a list of `Reasoning` objects.
            Output example:
            ```python
            LMOutput(
                response="Golden retriever is a good dog breed.",
                reasoning=[Reasoning(type="thinking", reasoning="Let me think about it...", signature="x")],
            )
            ```
        3. Streaming mode with `output_thinking = False`
            Return a string of the response.
            Stream the response token with the `EventType.RESPONSE` event.
            Output example:
            ```python
            "Golden retriever is a good dog breed."
            ```
            Streaming output example:
            ```python
            {"type": "response", "value": "Golden retriever ", ...}
            {"type": "response", "value": "is a good dog breed.", ...}
            ```
        4. Streaming mode with `output_thinking = True`
            Return an `LMOutput` object that contains a `reasoning` attributes with a list of `Reasoning` objects.
            Stream the thinking token with the `EventType.DATA` event.
            Stream the response token with the `EventType.RESPONSE` event.
            Output example:
            ```python
            LMOutput(
                response="Golden retriever is a good dog breed.",
                reasoning=[Reasoning(type="thinking", reasoning="Let me think about it...", signature="x")],
            )
            ```
            Streaming output example:
            ```python
            {"type": "data", "value": "Let me think ", ...}
            {"type": "data", "value": "about it...", ...}
            {"type": "response", "value": "Golden retriever ", ...}
            {"type": "response", "value": "is a good dog breed.", ...}
            ```

        When both thinking and tool calling are enabled, the `output_thinking` parameter is required to be `True`.
        Otherwise, feeding back the tool results to the model after the tool calls are executed would throw an error,
        as it\'s required by Anthropic.

    Output types:
        The output of the `AnthropicLMInvoker` is of type `MultimodalOutput`, which is a type alias that can represent:
        1. `str`: The text response if no additional output is needed.
        2. `LMOutput`: A Pydantic model with the following attributes if any additional output is needed:
            2.1. response (str): The text response.
            2.2. tool_calls (list[ToolCall]): The tool calls, if the `tools` parameter is defined and the language model
                decides to invoke tools. Defaults to an empty list.
            2.3. structured_output (BaseModel | None): The structured output in the form of a Pydantic model,
                if the `response_schema` parameter is defined. Defaults to None.
            2.4. reasoning (list[Reasoning]): The reasoning objects, if the `use_thinking` and `output_thinking`
                parameters are set to `True`. Defaults to an empty list.
    '''
    client: Incomplete
    model_name: Incomplete
    response_schema: Incomplete
    use_thinking: Incomplete
    thinking_budget: Incomplete
    output_thinking: Incomplete
    def __init__(self, model_name: str, api_key: str, model_kwargs: dict[str, Any] | None = None, default_hyperparameters: dict[str, Any] | None = None, tools: list[Tool] | None = None, response_schema: BaseModel | None = None, use_thinking: bool = False, thinking_budget: int = ..., output_thinking: bool = False) -> None:
        """Initializes the AnthropicLmInvoker instance.

        Args:
            model_name (str): The name of the Anthropic language model.
            api_key (str): The Anthropic API key.
            model_kwargs (dict[str, Any] | None, optional): Additional keyword arguments for the Anthropic client.
            default_hyperparameters (dict[str, Any] | None, optional): Default hyperparameters for invoking the model.
                Defaults to None.
            tools (list[Tool] | None, optional): Tools provided to the language model to enable tool calling.
                Defaults to None.
            response_schema (BaseModel | None, optional): The schema of the response. If provided, a structured output
                in the form of a Pydantic model will be included in the output. Defaults to None.
            use_thinking (bool, optional): Whether to enable thinking. Defaults to False.
            thinking_budget (int, optional): The tokens allocated for the thinking process. Must be greater than or
                equal to 1024. Ignored if `use_thinking=False`. Defaults to DEFAULT_THINKING_BUDGET.
            output_thinking (bool, optional): Whether to output the thinking token. Ignored if `use_thinking=False`.
                Defaults to False.

        Raises:
            ValueError:
            1. `use_thinking` is True, but the `thinking_budget` is less than 1024.
            2. `use_thinking` is True and `tools` are provided, but `output_thinking` is False.
            3. `response_schema` is provided, but `tools` or `use_thinking` are also provided.
        """
