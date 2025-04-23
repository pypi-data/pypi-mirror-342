import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from gllm_core.event import EventEmitter as EventEmitter
from gllm_core.schema import Chunk, Component
from typing import Any

RETURN_TYPE_CHUNKS: str
RETURN_TYPE_STRINGS: str
ReturnType: Incomplete

class BaseGraphRAGRetriever(Component, ABC, metaclass=abc.ABCMeta):
    """An abstract base class for the graph RAG retriever used in Gen AI applications.

    This class defines the interface for retriever components, which are responsible
    for retrieving relevant documents or information based on a given query.
    """
    @abstractmethod
    async def retrieve(self, query: str, retrieval_params: dict[str, Any] | None = None, event_emitter: EventEmitter | None = None, **kwargs: Any) -> str | list[str] | list[Chunk] | dict[str, Any]:
        '''Retrieve documents based on the query.

        This method should be implemented by subclasses to define the specific retrieval logic.

        Args:
            query (str): The query string to retrieve documents.
            retrieval_params (dict[str, Any] | None, optional): Additional parameters for the retrieval process.
                These could include \'max_results\', \'sort_order\', etc., specific to the retrieval logic.
                Defaults to None.
            event_emitter (EventEmitter | None, optional): The event emitter to emit events. Defaults to None.
            **kwargs (Any): Additional keyword arguments that may be needed for the retrieval process.
                Supported kwargs:
                - return_type (ReturnType): Type of return value ("chunks" or "strings"). Defaults to "chunks".

        Returns:
            str | list[str] | list[Chunk] | dict[str, Any]: The result of the retrieval process based on return_type:
                - If return_type is "chunks": Returns list[Chunk]
                - If return_type is "strings": Returns list[str]
                - Returns empty list on error

        Raises:
            NotImplementedError: If the method is not implemented.
        '''
