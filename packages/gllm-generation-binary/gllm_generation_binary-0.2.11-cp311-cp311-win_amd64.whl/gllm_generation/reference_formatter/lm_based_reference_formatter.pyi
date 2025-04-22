from _typeshed import Incomplete
from gllm_core.schema import Chunk as Chunk
from gllm_generation.reference_formatter.reference_formatter import BaseReferenceFormatter as BaseReferenceFormatter
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor, UsesLM
from typing import Callable

DEFAULT_BATCH_SIZE: int
DEFAULT_REFERENCE_METADATA: str

class LMBasedReferenceFormatter(BaseReferenceFormatter, UsesLM):
    '''A reference formatter that utilizes a language model to filter the candidate chunks.

    This class extends the BaseReferenceFormatter and uses a language model to process and filter a list of
    candidate chunks. The language model filters the chunks based on the content and selected metadata of the chunks.
    It then formats the relevant chunks into a reference string or a list of chunks depending on the `stringify`
    attribute.

    Attributes:
        lm_request_processor (LMRequestProcessor): The request processor used to handle the candidate chunks filtering.
        batch_size (int): The number of chunks to process in each batch.
        stringify (bool): Whether to format the references as a string. If False, the references will be returned as a
            list of chunks.
        format_references_func (Callable[[list[str]], str]): A function that formats a list of formatted chunks
            as a string of references.
        format_chunk_func (Callable[[Chunk], str]): A function that formats a chunk as a reference.
        streamable (bool): A flag to indicate whether the formatted references will be streamed if an event emitter is
            provided.

    Notes:
        When defining the `lm_request_processor`, you must carefully pay attention to the value of `reference_metadata`,
        as it will define:
        1. The format of the context sent to the `lm_request_processor`.
        2. The JSON object returned by the `lm_request_processor`.

        For example, if the value of the `reference_metadata` is `file_name`, the context sent to the
        `lm_request_processor` will be as follows:
        ```
        [CHUNK]
        file_name: <file_name_1>
        content:
        <content_1>

        [CHUNK]
        file_name: <file_name_2>
        content:
        <content_2>
        ```
        The `lm_request_processor` must be configured to:
        1. Take 2 variables as its input:
           1. `response`: The synthesized response.
           2. `context`: The formatted context string of the candidate chunks.
        2. Return a JSON object (Which can be configured using the `JSONOutputParser`) with a `file_name` key
           containing the list of `file_name` of the relevant chunks. For example:
           ```
           {
               "file_name": ["<file_name_1>", "<file_name_3>"]
           }
           ```
    '''
    lm_request_processor: Incomplete
    batch_size: Incomplete
    reference_metadata: Incomplete
    def __init__(self, lm_request_processor: LMRequestProcessor, batch_size: int = ..., reference_metadata: str = ..., stringify: bool = True, format_references_func: Callable[[list[str]], str] | None = None, format_chunk_func: Callable[[Chunk], str] | None = None, format_chunk_metadata_map: dict[str, str] | None = None, streamable: bool = True) -> None:
        """Initializes a new instance of the LMBasedReferenceFormatter class.

        Args:
            lm_request_processor (LMRequestProcessor): The request processor used to handle the candidate chunks
                filtering.
            batch_size (int, optional): The number of chunks to process in each batch. Defaults to DEFAULT_BATCH_SIZE.
            reference_metadata (str, optional): The metadata of the chunk to be referenced by the language model in the
                filtering process. Defaults to DEFAULT_REFERENCE_METADATA.
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
