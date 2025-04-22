from _typeshed import Incomplete
from gllm_core.event import EventEmitter as EventEmitter
from gllm_generation.response_synthesizer.response_synthesizer import BaseResponseSynthesizer as BaseResponseSynthesizer
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor, UsesLM
from gllm_inference.schema import PromptRole as PromptRole
from typing import Any

class StuffResponseSynthesizer(BaseResponseSynthesizer, UsesLM):
    '''A response synthesizer that synthesizes response using the stuff technique.

    The `StuffResponseSynthesizer` class implements the `BaseResponseSynthesizer` by using a language model request
    processor to generate a response based on the provided query. It employs the "stuff" technique, where the optional
    input `query` and other input variables passed through `state_variables` are processed to create the prompt for
    the language model and the response is generated in a single language model call.

    Attributes:
        lm_request_processor (LMRequestProcessor): The request processor used to handle the response generation.
        streamable (bool): A flag to indicate whether the synthesized response will be streamed if an event emitter is
            provided.
    '''
    lm_request_processor: Incomplete
    def __init__(self, lm_request_processor: LMRequestProcessor, streamable: bool = True) -> None:
        """Initializes a new instance of the StuffResponseSynthesizer class.

        Args:
            lm_request_processor (LMRequestProcessor): The request processor used to handle the response generation.
            streamable (bool, optional): A flag to indicate whether the synthesized response will be streamed if an
                event emitter is provided. Defaults to True.
        """
    async def synthesize_response(self, query: str | None = None, state_variables: dict[str, Any] | None = None, history: list[tuple[PromptRole, str | list[Any]]] | None = None, event_emitter: EventEmitter | None = None, system_multimodal_contents: list[Any] | None = None, user_multimodal_contents: list[Any] | None = None) -> str:
        """Synthesizes the response using the provided query and state variables.

        This method takes the input `query` and additional `state_variables`, integrates them into `prompt_kwargs`,
        and passes them to the `LMRequestProcessor` for processing. The synthesized response is then returned.

        Args:
            query (str | None, optional): The input query for generating the response. Defaults to None.
            state_variables (dict[str, Any] | None, optional): Additional state variables to include in the prompt.
                Defaults to None.
            history (list[tuple[PromptRole, str | list[Any]]] | None, optional): The chat history of the conversation
                to be considered in generating the response. Defaults to None.
            event_emitter (EventEmitter | None, optional): The event emitter for handling events during response
                synthesis. Defaults to None.
            system_multimodal_contents (list[Any] | None, optional): The system multimodal contents to be considered
                in generating the response. Defaults to None.
            user_multimodal_contents (list[Any] | None, optional): The user multimodal contents to be considered in
                generating the response. Defaults to None.

        Returns:
            str: The synthesized response from the language model.
        """
