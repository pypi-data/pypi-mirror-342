import abc
from abc import ABC, abstractmethod
from gllm_core.schema import Chunk, Component

class BaseReranker(Component, ABC, metaclass=abc.ABCMeta):
    """An abstract base class for the rerankers used in Gen AI applications."""
    @abstractmethod
    async def rerank(self, chunks: list[Chunk], query: str | None = None) -> list[Chunk]:
        """Rerank the list of chunks.

        This abstract method must be implemented by subclasses to define how to rerank the list of chunks.
        It is expected to return a list of reranked chunks.

        Args:
            chunks (list[Chunk]): The list of chunks to be reranked.
            query (str | None, optional): The query to be used for reranking. Defaults to None.

        Returns:
            list[Chunk]: A list of reranked chunks.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
