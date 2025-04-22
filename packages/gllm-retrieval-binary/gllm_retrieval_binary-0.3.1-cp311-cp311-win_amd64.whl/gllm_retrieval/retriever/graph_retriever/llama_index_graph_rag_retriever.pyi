from gllm_core.event import EventEmitter as EventEmitter
from gllm_core.schema import Chunk
from gllm_datastore.graph_data_store.llama_index_graph_rag_data_store import LlamaIndexGraphRAGDataStore as LlamaIndexGraphRAGDataStore
from gllm_retrieval.retriever.graph_retriever.graph_rag_retriever import BaseGraphRAGRetriever as BaseGraphRAGRetriever, RETURN_TYPE_CHUNKS as RETURN_TYPE_CHUNKS, RETURN_TYPE_STRINGS as RETURN_TYPE_STRINGS
from gllm_retrieval.retriever.graph_retriever.util import clean_cypher_query as clean_cypher_query
from llama_index.core.base.embeddings.base import BaseEmbedding as BaseEmbedding
from llama_index.core.base.llms.base import BaseLLM as BaseLLM
from llama_index.core.graph_stores.types import PropertyGraphStore as PropertyGraphStore
from llama_index.core.indices.property_graph import PGRetriever
from llama_index.core.vector_stores.types import BasePydanticVectorStore as BasePydanticVectorStore
from typing import Any

class LlamaIndexGraphRAGRetriever(BaseGraphRAGRetriever):
    """A retriever class for querying a knowledge graph using the LlamaIndex framework.

    Attributes:
        _index (PropertyGraphIndex): The property graph index to use.
        _graph_store (LlamaIndexGraphRAGDataStore | PropertyGraphStore): The graph store to use.
        _llm (BaseLLM | None): The language model to use.
        _embed_model (BaseEmbedding | None): The embedding model to use.
        _property_graph_retriever (PGRetriever): The property graph retriever to use.
        _logger (logging.Logger): The logger to use.
        _default_return_type (ReturnType): The default return type for retrieve method.
    """
    def __init__(self, data_store: LlamaIndexGraphRAGDataStore | PropertyGraphStore, property_graph_retriever: PGRetriever | None = None, llama_index_llm: BaseLLM | None = None, embed_model: BaseEmbedding | None = None, vector_store: BasePydanticVectorStore | None = None, **kwargs: Any) -> None:
        '''Initializes the LlamaIndexGraphRAGRetriever with the provided components.

        Args:
            data_store (LlamaIndexGraphRAGDataStore | PropertyGraphStore): The graph store to use.
            property_graph_retriever (PGRetriever | None, optional): An existing retriever to use.
            llama_index_llm (BaseLLM | None, optional): The language model to use for text-to-Cypher retrieval.
            embed_model (BaseEmbedding | None, optional): The embedding model to use.
            vector_store (BasePydanticVectorStore | None, optional): The vector store to use.
            **kwargs (Any): Additional keyword arguments.
                Supported kwargs:
                - default_return_type (ReturnType): Default return type for retrieve method. Defaults to "chunks".

        Raises:
            ValueError: If an invalid return type is provided.
        '''
    async def retrieve(self, query: str, retrieval_params: dict[str, Any] | None = None, event_emitter: EventEmitter | None = None, **kwargs: Any) -> str | list[str] | list[Chunk] | dict[str, Any]:
        '''Retrieves relevant documents for a given query.

        Args:
            query (str): The query string to search for.
            retrieval_params (dict[str, Any] | None, optional): Additional retrieval parameters.
            event_emitter (EventEmitter | None, optional): Event emitter for logging.
            **kwargs (Any): Additional keyword arguments.
                Supported kwargs:
                - return_type (ReturnType): Type of return value ("chunks" or "strings").
                  Defaults to value set in constructor.

        Returns:
            str | list[str] | list[Chunk] | dict[str, Any]: The result of the retrieval process based on return_type:
                - If return_type is "chunks": Returns list[Chunk]
                - If return_type is "strings": Returns list[str]
                - Returns empty list on error

        Raises:
            ValueError: If an invalid return type is provided.
        '''
