import abc
from abc import ABC, abstractmethod
from gllm_core.schema import Chunk, Component

class BaseChunkProcessor(Component, ABC, metaclass=abc.ABCMeta):
    """An abstract base class for the chunk processors used in Gen AI applications."""
    @abstractmethod
    async def process_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        """Processes the given list of chunks.

        This abstract method must be implemented by subclasses to define how the chunks are processed. It is
        expected to return a list of processed chunks.

        Args:
            chunks (list[Chunk]): The list of chunks to be processed.

        Returns:
            list[Chunk]: A list of processed chunks.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
