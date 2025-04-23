from gllm_retrieval.query_transformer.query_transformer import BaseQueryTransformer as BaseQueryTransformer

class NoOpQueryTransformer(BaseQueryTransformer):
    """A query transformer that returns the input query without modification."""
    def __init__(self) -> None:
        """Initialize the NoOpQueryTransformer without an LM request processor."""
    async def transform(self, query: str | list[str] | dict[str, str]) -> list[str]:
        """Returns the input query as a single-element list without any transformation.

        Args:
            query (str | list[str] | dict[str, str]): The query, list of queries, or dictionary of queries
                to be transformed.

        Returns:
            list[str]: The original query or queries.
        """
    @classmethod
    def from_lm_components(cls, *args, **kwargs) -> NoOpQueryTransformer:
        """Create a NoOpQueryTransformer instance.

        Returns:
            NoOpQueryTransformer: A new instance of NoOpQueryTransformer.
        """
