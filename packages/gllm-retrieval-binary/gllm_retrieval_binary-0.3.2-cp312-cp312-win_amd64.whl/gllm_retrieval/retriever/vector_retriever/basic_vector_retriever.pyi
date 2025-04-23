from gllm_core.event import EventEmitter as EventEmitter
from gllm_core.schema import Chunk as Chunk
from gllm_datastore.vector_data_store.vector_data_store import BaseVectorDataStore as BaseVectorDataStore
from gllm_retrieval.constants import DEFAULT_RETRIEVAL_PARAMS as DEFAULT_RETRIEVAL_PARAMS, DEFAULT_TOP_K as DEFAULT_TOP_K
from gllm_retrieval.retriever.vector_retriever.vector_retriever import BaseVectorRetriever as BaseVectorRetriever

class BasicVectorRetriever(BaseVectorRetriever):
    """Initializes a new instance of the BasicVectorRetriever class.

    This class provides a straightforward implementation of the BaseRetriever,
    using a single data store for document retrieval.

    Attributes:
        data_store (BaseVectorDataStore): The data store used for retrieval operations.
    """
    def __init__(self, data_store: BaseVectorDataStore) -> None:
        """Initializes a new instance of the BasicRetriever class.

        Args:
            data_store (BaseVectorDataStore): The data store to be used for retrieval operations.
        """
