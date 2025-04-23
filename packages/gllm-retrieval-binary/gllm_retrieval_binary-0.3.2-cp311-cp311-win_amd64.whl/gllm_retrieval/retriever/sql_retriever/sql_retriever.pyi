import abc
import pandas as pd
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from gllm_core.event import EventEmitter as EventEmitter
from gllm_core.schema import Component
from gllm_datastore.sql_data_store.sql_data_store import BaseSQLDataStore as BaseSQLDataStore
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor
from typing import Any, Callable

class BaseSQLRetriever(Component, ABC, metaclass=abc.ABCMeta):
    """An abstract base class for the SQL database retriever used in Gen AI applications.

    This class defines the interface for SQL database retriever, which are responsible
    for retrieving data or information based on a given query.

    Attributes:
        sql_data_store (BaseSQLDataStore): The SQL database data store to be used.
        lm_request_processor (LMRequestProcessor | None): The LMRequestProcessor instance to be used for modifying a
            failed query. If not None, will modify the query upon failure.
        extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]]): A function to extract
            the modified query from the LM output.
        preprocess_query_func (Callable[[str], str] | None): A function to preprocess the query before execution.
    """
    sql_data_store: Incomplete
    lm_request_processor: Incomplete
    extract_func: Incomplete
    preprocess_query_func: Incomplete
    def __init__(self, sql_data_store: BaseSQLDataStore, lm_request_processor: LMRequestProcessor | None = None, extract_func: Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]] = None, preprocess_query_func: Callable[[str], str] | None = None) -> None:
        """Initializes the BaseSQLRetriever object.

        Args:
            sql_data_store (BaseSQLDataStore): The SQL database data store to be used.
            lm_request_processor (LMRequestProcessor | None, optional): The LMRequestProcessor instance to be used
                for modifying a failed query. If not None, will modify the query upon failure.
            extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]], optional): A
                function to extract the transformed query from the output. Defaults to None, in which case a default
                extractor will be used.
            preprocess_query_func (Callable[[str], str] | None, optional): A function to preprocess the query before.
                Defaults to None.
        """
    @abstractmethod
    async def retrieve(self, query: str, event_emitter: EventEmitter | None = None, prompt_kwargs: dict[str, Any] | None = None, return_query: bool = False) -> pd.DataFrame | tuple[str, pd.DataFrame]:
        """Retrieve data based on the query.

        This method should be implemented by subclasses to define the specific retrieval logic.

        Args:
            query (str): The query string to retrieve data.
            event_emitter (EventEmitter | None, optional): The event emitter to emit events. Defaults to None.
            prompt_kwargs (dict[str, Any] | None, optional): Additional keyword arguments for the prompt.
                Defaults to None.
            return_query (bool, optional): If True, returns a tuple of the executed query and the result.
                If False, returns only the result. Defaults to False.

        Returns:
            pd.DataFrame | tuple[str, pd.DataFrame]: The result of the retrieval process.
                If return_query is True, returns a tuple of the executed query and the result.
                If return_query is False, returns only the result.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
