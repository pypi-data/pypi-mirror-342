from _typeshed import Incomplete
from gllm_core.schema import Chunk as Chunk
from gllm_inference.em_invoker.em_invoker import BaseEMInvoker as BaseEMInvoker
from gllm_retrieval.reranker.reranker import BaseReranker as BaseReranker
from typing import Callable

class SimilarityBasedReranker(BaseReranker):
    """A class to rerank chunks based on their similarity to a given query.

    Attributes:
        embeddings (BaseEMInvoker): An instance of the BaseEMInvoker class to embed text.
        similarity_func (Callable[[list[float], list[float]], float]): A callback function to calculate the similarity.
    """
    similarity_func: Incomplete
    embeddings: Incomplete
    def __init__(self, embeddings: BaseEMInvoker, similarity_func: Callable[[list[float], list[float]], float] = ...) -> None:
        """Initializes the SimilarityBasedReranker class with a similarity function.

        This constructor method initializes an instance of the SimilarityBasedReranker class, setting up the similarity
        function that will be used to rerank chunks based on their similarity to a query.

        Args:
            embeddings (BaseEMInvoker):
                An instance of the BaseEMInvoker class that will be used to calculate the embeddings of the query and
                the chunks.
            similarity_func (Callable[[list[float], list[float]], float]):
                A callback function that takes two parameters (the query embeddings and chunk embeddings),
                and returns a similarity score as a float. Defaults to cosine similarity.

        Returns:
            None
        """
    async def rerank(self, chunks: list[Chunk], query: str | None = None) -> list[Chunk]:
        """Reranks a list of chunks based on similarity to a given query.

        This function takes a list of chunks and a query, then reranks the chunks
        based on their score in descending order (higher score means higher similarity).
        The similarity score is calculated using a predefined similarity function.

        Args:
            chunks (list[Chunk]): A list of Chunk objects to be reranked.
            query (str | None, optional): The query to be used for reranking. Defaults to None.

        Returns:
            list[Chunk]: A list of Chunk objects reranked based on similarity to the query.
        """
