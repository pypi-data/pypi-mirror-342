from enum import StrEnum
from pydantic import BaseModel
from typing import Any

class ToolCall(BaseModel):
    """Defines a tool call request when a language model decides to invoke a tool.

    Attributes:
        id (str): The ID of the tool call.
        name (str): The name of the tool.
        args (dict[str, Any]): The arguments of the tool call.
    """
    id: str
    name: str
    args: dict[str, Any]

class ToolResult(BaseModel):
    """Defines a tool result to be sent back to the language model.

    Attributes:
        id (str): The ID of the tool call.
        output (str): The output of the tool call.
    """
    id: str
    output: str

class Reasoning(BaseModel):
    """Defines a reasoning output when a language model is configured to use reasoning.

    Attributes:
        reasoning (str): The reasoning text. Defaults to an empty string.
        type (str): The type of the reasoning output. Defaults to an empty string.
        data (str): The additional data of the reasoning output. Defaults to an empty string.
    """
    reasoning: str
    type: str
    data: str

class LMOutput(BaseModel):
    """Defines the output of a language model.

    Attributes:
        response (str): The text response. Defaults to an empty string.
        tool_calls (list[ToolCall]): The tool calls, if the language model decides to invoke tools.
            Defaults to an empty list.
        structured_output (BaseModel | None): The structured output in the form of a Pydantic model,
            if a response schema is defined for the language model. Defaults to None.
        reasoning (list[Reasoning]): The reasoning, if the language model is configured to output reasoning.
            Defaults to an empty list.
    """
    response: str
    tool_calls: list[ToolCall]
    structured_output: BaseModel | None
    reasoning: list[Reasoning]

class PromptRole(StrEnum):
    """Defines valid prompt roles."""
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'

class MimeType(StrEnum):
    """Defines valid mime types."""
    IMAGE = 'image'
UnimodalContent = str | list[str | ToolCall] | list[ToolResult]
UnimodalPrompt = list[tuple[PromptRole, UnimodalContent]]
MultimodalContent = str | bytes | ToolCall | ToolResult | Reasoning
MultimodalPrompt = list[tuple[PromptRole, list[MultimodalContent]]]
MultimodalOutput = str | LMOutput
