from _typeshed import Incomplete
from gllm_core.schema import Chunk
from gllm_core.utils import ChunkMetadataMerger
from gllm_retrieval.chunk_processor.chunk_processor import BaseChunkProcessor as BaseChunkProcessor
from gllm_retrieval.constants import DUPES_METADATA as DUPES_METADATA, MERGED_IDS_METADATA as MERGED_IDS_METADATA
from typing import Callable

NULL_CHUNK_ID: str

class MergingChunkProcessor(BaseChunkProcessor):
    """A chunk processor that gathers and merges together adjacent chunks.

    The `MergingChunkProcessor` class identifies related chunks based on their adjacent chunk IDs,
    merges the related chunks, and outputs a list of combined chunks. When merging chunks and their content,
    it handles overlaps and common prefixes to ensure smooth merging.

    Attributes:
        prev_chunk_id_metadata (str): The metadata key for the previous chunk ID.
        next_chunk_id_metadata (str): The metadata key for the next chunk ID.
        id_merger_func (Callable[[list[str]], str]): The function used to merge the IDs of merged chunks. The function
            should receive a list of IDs of the chunks that are being merged and the output will be used as the ID of
            the merged chunk.
        content_merger_func (Callable[[list[str]], str]): The function used to merge the content of merged chunks. The
            function should receive a list of contents of the chunks that are being merged and the output will be used
            as the content of the merged chunk.
        metadata_merger (ChunkMetadataMerger): The metadata merger used to merge the metadata of merged chunks. The
            merger should receive a list of metadata of the chunks that are being merged and the output will be used as
            the metadata of the merged chunk.
    """
    prev_chunk_id_metadata: Incomplete
    next_chunk_id_metadata: Incomplete
    id_merger_func: Incomplete
    content_merger_func: Incomplete
    metadata_merger: Incomplete
    def __init__(self, prev_chunk_id_metadata: str = ..., next_chunk_id_metadata: str = ..., id_merger_func: Callable[[list[str]], str] = ..., content_merger_func: Callable[[list[str]], str] = ..., metadata_merger: ChunkMetadataMerger | None = None) -> None:
        """Initializes a new instance of the MergingChunkProcessor class.

        Args:
            prev_chunk_id_metadata (str, optional): The metadata key for the previous chunk ID.
                Defaults to `DefaultChunkMetadata.PREV_CHUNK_ID`.
            next_chunk_id_metadata (str, optional): The metadata key for the next chunk ID.
                Defaults to `DefaultChunkMetadata.NEXT_CHUNK_ID`.
            id_merger_func (Callable[[list[str]], str], optional): The function used to merge the IDs of merged chunks.
                The function should receive a list of IDs of the chunks that are being merged and the output will be
                used as the ID of the merged chunk. Defaults to `MergerMethod.concatenate()`.
            content_merger_func (Callable[[list[str]], str], optional): The function used to merge the content of
                merged chunks. The function should receive a list of contents of the chunks that are being merged
                and the output will be used as the content of the merged chunk.
                Defaults to `MergerMethod.merge_overlapping_strings()`.
            metadata_merger (ChunkMetadataMerger | None, optional): The metadata merger used to merge the metadata of
                merged chunks. The merger should receive a list of metadata of the chunks that are being merged and
                the output will be used as the metadata of the merged chunk. Defaults to None, in which case a
                default `ChunkMetadataMerger()` is used.
        """
    async def process_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        """Processes a list of chunks by gathering and merging related chunks.

        This method iterates through the provided list of chunks, gathers related chunks, and merges them.

        Args:
            chunks (list[Chunk]): The list of chunks to be processed.

        Returns:
            list[Chunk]: A list of merged chunks, where related chunks are combined into a single chunk.
        """
