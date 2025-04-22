from _typeshed import Incomplete
from gllm_core.schema import Chunk as Chunk
from gllm_generation.reference_formatter.reference_formatter import BaseReferenceFormatter as BaseReferenceFormatter
from gllm_inference.em_invoker.em_invoker import BaseEMInvoker as BaseEMInvoker
from typing import Callable

DEFAULT_THRESHOLD: float

class SimilarityBasedReferenceFormatter(BaseReferenceFormatter):
    """A reference formatter that filters the candidate chunks based on their relevance to the synthesized response.

    This class extends the BaseReferenceFormatter and uses an embedding model to compute the similarity between
    the synthesized response and the chunk contents. It filters out chunks whose similarity score falls below
    a specified threshold. Then, it formats the relevant chunks into a reference string or a list of chunks
    depending on the `stringify` attribute.

    Attributes:
        em_invoker (BaseEMInvoker): The embedding model invoker for generating embeddings for the response and
            chunk contents.
        threshold (float): The similarity threshold for filtering chunks.
        stringify (bool): Whether to format the references as a string. If False, the references will be returned as a
            list of chunks.
        format_references_func (Callable[[list[str]], str]): A function that formats a list of formatted chunks
            as a string of references.
        format_chunk_func (Callable[[Chunk], str]): A function that formats a chunk as a reference.
        streamable (bool): A flag to indicate whether the formatted references will be streamed if an event emitter is
            provided.
    """
    em_invoker: Incomplete
    threshold: Incomplete
    def __init__(self, em_invoker: BaseEMInvoker, threshold: float = ..., stringify: bool = True, format_references_func: Callable[[list[str]], str] | None = None, format_chunk_func: Callable[[Chunk], str] | None = None, format_chunk_metadata_map: dict[str, str] | None = None, streamable: bool = True) -> None:
        """Initializes a new instance of the SimilarityBasedReferenceFormatter class.

        Args:
            em_invoker (BaseEMInvoker): The embedding model invoker for generating embeddings for the response and
                chunk contents.
            threshold (float, optional): The similarity threshold for filtering chunks. Defaults to DEFAULT_THRESHOLD.
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
