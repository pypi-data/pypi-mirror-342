import abc
from _typeshed import Incomplete
from abc import ABC
from gllm_core.event import EventEmitter as EventEmitter
from gllm_core.schema import Chunk as Chunk, Component
from gllm_datastore.vector_data_store.vector_data_store import BaseVectorDataStore as BaseVectorDataStore
from gllm_retrieval.constants import DEFAULT_TOP_K as DEFAULT_TOP_K
from typing import Any

class BaseVectorRetriever(Component, ABC, metaclass=abc.ABCMeta):
    """An abstract base class for the retriever used in Gen AI applications.

    This class defines the interface for retriever components, which are responsible
    for retrieving relevant documents or information based on a given query.

    Attributes:
        data_store (BaseVectorDataStore | list[BaseVectorDataStore]): The data store or list of data stores to be used.
    """
    data_store: Incomplete
    def __init__(self, data_store: BaseVectorDataStore | list[BaseVectorDataStore]) -> None:
        """Initializes the BaseRetriever object.

        Args:
            data_store (BaseVectorDataStore | list[BaseVectorDataStore]):
                The data store or list of data stores to be used.
        """
    async def retrieve(self, query: str, top_k: int = ..., retrieval_params: dict[str, Any] | None = None, event_emitter: EventEmitter | None = None, timeout: float | int | None = None) -> list[Chunk]:
        """Retrieve documents based on the query.

        This method performs the retrieval process by calling the `_retrieve` method.
        If the retrieval process fails or times out, it will return an empty list.

        Args:
            query (str): The query string to retrieve documents.
            top_k (int, optional): The maximum number of documents to retrieve. Defaults to DEFAULT_TOP_K.
            retrieval_params (dict[str, Any] | None, optional): Additional parameters for the retrieval process.
                These could include 'max_results', 'sort_order', etc., specific to the retrieval logic.
                Defaults to None.
            event_emitter (EventEmitter | None, optional): The event emitter to emit events. Defaults to None.
            timeout (float | int | None, optional): Maximum time in seconds to wait for retrieval to complete.
                If None, no timeout is applied. Defaults to None.

        Returns:
            list[Chunk]: A list of retrieved documents.
        """
