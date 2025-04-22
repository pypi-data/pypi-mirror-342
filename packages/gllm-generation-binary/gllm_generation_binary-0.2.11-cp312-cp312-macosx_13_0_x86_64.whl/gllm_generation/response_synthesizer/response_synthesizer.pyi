import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from gllm_core.event import EventEmitter as EventEmitter
from gllm_core.schema import Component
from gllm_inference.schema import PromptRole as PromptRole
from typing import Any

class BaseResponseSynthesizer(Component, ABC, metaclass=abc.ABCMeta):
    """An abstract base class for the response synthesizers used in Gen AI applications.

    The `BaseResponseSynthesizer` class provides a framework for synthesizing responses based on input queries.
    Subclasses must implement the `synthesize_response` method to define how the response is generated.

    Attributes:
        streamable (bool): A flag to indicate whether the synthesized response will be streamed if an event emitter is
            provided.
    """
    streamable: Incomplete
    def __init__(self, streamable: bool = True) -> None:
        """Initializes a new instance of the `BaseResponseSynthesizer` class.

        Args:
            streamable (bool, optional): A flag to indicate whether the synthesized response will be streamed if an
                event emitter is provided. Defaults to True.
        """
    @abstractmethod
    async def synthesize_response(self, query: str | None = None, state_variables: dict[str, Any] | None = None, history: list[tuple[PromptRole, str | list[Any]]] | None = None, event_emitter: EventEmitter | None = None, system_multimodal_contents: list[Any] | None = None, user_multimodal_contents: list[Any] | None = None) -> str:
        """Synthesizes a response based on the provided query.

        This abstract method must be implemented by subclasses to define the logic for generating a response. It
        may optionally take an input `query`, some other input variables passed through `state_variables`, and an
        `event_emitter`. It returns the synthesized response as a string.

        Args:
            query (str | None, optional): The input query used to synthesize the response. Defaults to None.
            state_variables (dict[str, Any] | None, optional): Additional state variables to assist in generating the
                response. Defaults to None.
            history (list[tuple[PromptRole, str | list[Any]]] | None, optional): The chat history of the conversation
                to be considered in generating the response. Defaults to None.
            event_emitter (EventEmitter | None, optional): The event emitter for handling events during response
                synthesis. Defaults to None.
            system_multimodal_contents (list[Any] | None, optional): The system multimodal contents to be considered
                in generating the response. Defaults to None.
            user_multimodal_contents (list[Any] | None, optional): The user multimodal contents to be considered in
                generating the response. Defaults to None.

        Returns:
            str: The synthesized response.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
