import abc
from _typeshed import Incomplete
from abc import ABC
from gllm_core.event import EventEmitter as EventEmitter
from gllm_core.schema import Chunk, Component
from typing import Callable

def format_references_as_string(formatted_chunks: list[str]) -> str:
    """Formats a list of formatted chunks as a string of references.

    Args:
        formatted_chunks (list[str]): A list of formatted chunks.

    Returns:
        str: A string of references.
    """
def format_chunk_as_string(metadata_map: dict[str, str]) -> Callable[[Chunk], str]:
    """Creates a function that formats a chunk as a string of reference.

    Args:
        metadata_map (dict[str, str]): A dictionary mapping the metadata keys to the chunk metadata keys.

    Returns:
        Callable[[Chunk], str]: A function that formats a chunk as a string of reference.
    """

DEFAULT_FORMAT_CHUNK_METADATA_MAP: Incomplete

class BaseReferenceFormatter(Component, ABC, metaclass=abc.ABCMeta):
    """An abstract base class for the reference formatters used in Gen AI applications.

    The `BaseReferenceFormatter` class provides a framework for formatting references based on the synthesized
    response and retrieved chunks. It first retrieves the relevant chunks based on the synthesized response, then
    formats the references as a string or a list of chunks depending on the `stringify` attribute. Subclasses must
    implement the `_get_relevant_chunks` method to retrieve the relevant chunks.

    Attributes:
        stringify (bool): Whether to format the references as a string. If False, the references will be returned as a
            list of chunks.
        format_references_func (Callable[[list[str]], str]): A function that formats a list of formatted chunks
            as a string of references.
        format_chunk_func (Callable[[Chunk], str]): A function that formats a chunk as a reference.
        streamable (bool): A flag to indicate whether the formatted references will be streamed if an event emitter is
            provided.
    """
    stringify: Incomplete
    format_references_func: Incomplete
    format_chunk_func: Incomplete
    streamable: Incomplete
    def __init__(self, stringify: bool = True, format_references_func: Callable[[list[str]], str] | None = None, format_chunk_func: Callable[[Chunk], str] | None = None, format_chunk_metadata_map: dict[str, str] | None = None, streamable: bool = True) -> None:
        """Initializes a new instance of the BaseReferenceFormatter class.

        Args:
            stringify (bool, optional): Whether to format the references as a string. If False, the references will be
                returned as a list of chunks. Defaults to True.
            format_references_func (Callable[[list[str]], str] | None, optional): A function that formats a list of
                formatted chunks as a string of references. Defaults to None, in which case
                `format_references_as_string` will be used.
            format_chunk_func (Callable[[Chunk], str] | None, optional): A function that formats a chunk as a reference.
                Defaults to None, in which case `format_chunk_as_string` will be used.
            format_chunk_metadata_map (dict[str, str] | None, optional): A dictionary mapping the metadata keys needed
                by the `format_chunk_func` to the actual chunk metadata keys. The keys in the dictionary must match the
                metadata keys needed by the `format_chunk_func`. Defaults to None, in which case
                `DEFAULT_FORMAT_CHUNK_METADATA_MAP` will be used.
            streamable (bool, optional): A flag to indicate whether the formatted references will be streamed if an
                event emitter is provided. Defaults to True.
        """
    async def format_reference(self, response: str, chunks: list[Chunk], event_emitter: EventEmitter | None = None) -> str | list[Chunk]:
        """Formats references based on the synthesized response and retrieved chunks.

        This method formats references based on the synthesized response and retrieved chunks. First, it retrieves the
        chunks that are relevant to the response. Then, it formats the references as a string if the `stringify`
        attribute is set to `True`. It also streams the formatted references to the event emitter if provided.

        Args:
            response (str): The synthesized response.
            chunks (list[Chunk]): A list of Chunk objects used to generate the references.
            event_emitter (EventEmitter | None, optional): The optional event emitter to stream the formatted reference.
                Defaults to None.

        Returns:
            str | list[Chunk]: The formatted references as a string or a list of chunks.
        """
