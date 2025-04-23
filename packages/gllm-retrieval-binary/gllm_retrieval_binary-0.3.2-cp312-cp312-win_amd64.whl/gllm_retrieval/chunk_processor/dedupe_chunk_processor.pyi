from gllm_core.schema import Chunk
from gllm_retrieval.chunk_processor.chunk_processor import BaseChunkProcessor as BaseChunkProcessor
from gllm_retrieval.constants import DUPES_METADATA as DUPES_METADATA

class DedupeChunkProcessor(BaseChunkProcessor):
    """A chunk processor that removes duplicate chunks.

    The `DedupeChunkProcessor` class provides functionality for processing a list of chunks by removing duplicates.
    The duplicates are determined based on the chunk's ID and content. It ensures that each chunk in the final list
    is unique, both in terms of its ID and its content.

    Attributes:
        None
    """
    async def process_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        """Processes a list of chunks by removing duplicate chunks.

        This function processes a list of chunks by eliminating duplicates based on the chunk's ID and content hash.
        It uses SHA-256 hashing to efficiently compare chunk contents, saving memory compared to storing full content.
        It also adds a metadata to store the metadata of the chunks with duplicate content for the retained chunks,
        if any.

        Args:
            chunks (list[Chunk]): A list of Chunk objects to be processed.

        Returns:
            list[Chunk]: A list of unique Chunk objects with duplicates removed.
        """
