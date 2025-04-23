from _typeshed import Incomplete
from gllm_core.schema import Chunk as Chunk
from gllm_retrieval.reranker.reranker import BaseReranker as BaseReranker

class FlagEmbeddingReranker(BaseReranker):
    """Reranks a list of chunks using a flag embedding.

    Requires the `FlagEmbedding` package to be installed.

    Attributes:
        reranker (FlagReranker): The flag embedding reranker model.
    """
    reranker: Incomplete
    def __init__(self, model_path: str, use_fp16: bool = True) -> None:
        """Initializes a new instance of the FlagEmbeddingReranker class.

        Args:
            model_path (str): A path containing the reranker model.
            use_fp16 (bool): Whether to reduce the model size to FP16 or not. Defaults to True.
        """
    async def rerank(self, chunks: list[Chunk], query: str | None = None) -> list[Chunk]:
        """Rerank the list of chunks using the flag embedding reranker.

        This method calculates the score for each chunk based on the given query
        and reranks the chunks based on the score in descending order.

        Args:
            chunks (list[Chunk]): The list of chunks to be reranked.
            query (str | None, optional): The query to be used for reranking. Defaults to None.

        Returns:
            list[Chunk]: A list of reranked chunks.
        """
