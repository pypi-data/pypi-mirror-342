from _typeshed import Incomplete
from gllm_core.event import EventEmitter as EventEmitter
from gllm_generation.response_synthesizer.response_synthesizer import BaseResponseSynthesizer as BaseResponseSynthesizer
from gllm_inference.schema import PromptRole as PromptRole
from typing import Any

DEFAULT_RESPONSE_PREFIX: str
DEFAULT_FALLBACK_RESPONSE: str

class StaticListResponseSynthesizer(BaseResponseSynthesizer):
    """A response synthesizer that synthesizes a static list response.

    The `StaticListResponseSynthesizer` class generates a response by formatting a list of context items.
    If no context is provided, it returns a fallback response. The response can be prefixed with a customizable
    string and is intended for use when a simple list-based response is required.

    Attributes:
        response_prefix (str): The string prefix that precedes the list of items.
        fallback_response (str): The fallback response if the context list is empty.
        delimiter (str): The delimiter to be placed in between context list elements.
        streamable (bool): A flag to indicate whether the synthesized response will be streamed if an event emitter is
            provided.
    """
    preceding_line: Incomplete
    fallback_response: Incomplete
    delimiter: Incomplete
    def __init__(self, response_prefix: str = ..., fallback_response: str = ..., delimiter: str = '\n', streamable: bool = True) -> None:
        '''Initializes a new instance of the StaticListResponseSynthesizer class.

        Args:
            response_prefix (str, optional): The string prefix that precedes the list of items.
                Defaults to DEFAULT_RESPONSE_PREFIX.
            fallback_response (str, optional): The fallback response if the context list is empty.
                Defaults to DEFAULT_FALLBACK_RESPONSE.
            delimiter (str, optional): The delimiter to be placed in between context list elements. Defaults to "\\n".
            streamable (bool, optional): A flag to indicate whether the synthesized response will be streamed if an
                event emitter is provided. Defaults to True.
        '''
    async def synthesize_response(self, query: str | None = None, state_variables: dict[str, Any] | None = None, history: list[tuple[PromptRole, str | list[Any]]] | None = None, event_emitter: EventEmitter | None = None, system_multimodal_contents: list[Any] | None = None, user_multimodal_contents: list[Any] | None = None) -> str:
        """Synthesizes a static list response based on the provided `context_list`.

        This method generates a response using the items in the `context_list`. If the list is empty, it returns
        a fallback response. The list items are prefixed with a customizable preceding line and are numbered
        sequentially. If an `event_emitter` is provided, the response is emitted as an event.

        Args:
            query (str | None, optional): The input query. Unused in this synthesizer. Defaults to None.
            state_variables (dict[str, Any] | None, optional): A dictionary that must include a `context_list` key of
                type `list`. Defaults to None.
            history (list[tuple[PromptRole, str | list[Any]]] | None, optional): The chat history of the conversation
                to be considered in generating the response. Unused in this synthesizer. Defaults to None.
            event_emitter (EventEmitter | None, optional): The event emitter for handling events during response
                synthesis. Defaults to None.
            system_multimodal_contents (list[Any] | None, optional): The system multimodal contents to be considered
                in generating the response. Unused in this synthesizer. Defaults to None.
            user_multimodal_contents (list[Any] | None, optional): The user multimodal contents to be considered in
                generating the response. Unused in this synthesizer. Defaults to None.

        Returns:
            str: The synthesized list-based response or the fallback response.

        Raises:
            ValueError: If `context_list` is missing or is not of type `list`.
        """
