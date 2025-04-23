import pandas as pd
from _typeshed import Incomplete
from gllm_core.event import EventEmitter as EventEmitter
from gllm_datastore.sql_data_store.sql_data_store import BaseSQLDataStore as BaseSQLDataStore
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor
from gllm_retrieval.retriever.sql_retriever.sql_retriever import BaseSQLRetriever as BaseSQLRetriever
from gllm_retrieval.utils.sql_utils import format_sql_query as format_sql_query
from typing import Any, Callable

DEFAULT_RETRYER_SYSTEM_PROMPT: str

class BasicSQLRetriever(BaseSQLRetriever):
    """Initializes a new instance of the BasicSQLRetriever class.

    This class provides a straightforward implementation of the BasicSQLRetriever,
    using a single data store for document retrieval.

    Attributes:
        sql_data_store (BaseSQLDataStore): The SQL database data store to be used.
        lm_request_processor (LMRequestProcessor | None): The LMRequestProcessor instance to be used for modifying a
            failed query. If not None, will modify the query upon failure.
        extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]]): A function to extract
            the modified query from the LM output.
        max_retries (int): The maximum number of retries for the retrieval process.
        preprocess_query_func (Callable[[str], str] | None): A function to preprocess the query before execution.
        logger (Logger): The logger instance to be used for logging.
    """
    max_retries: Incomplete
    logger: Incomplete
    def __init__(self, sql_data_store: BaseSQLDataStore, lm_request_processor: LMRequestProcessor | None = None, extract_func: Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]] = None, max_retries: int = 0, preprocess_query_func: Callable[[str], str] | None = None) -> None:
        """Initializes the BasicSQLRetriever object.

        Args:
            sql_data_store (BaseSQLDataStore): The SQL database data store to be used.
            lm_request_processor (LMRequestProcessor | None, optional): The LMRequestProcessor instance to be used
                for modifying a failed query. If not None, will modify the query upon failure.
            extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]], optional): A
                function to extract the transformed query from the output. Defaults to None, in which case a default
                extractor will be used.
            max_retries (int, optional): The maximum number of retries for the retrieval process. Defaults to 0.
            preprocess_query_func (Callable[[str], str] | None, optional): A function to preprocess the query before.
                Defaults to None.

        Raises:
            ValueError: If lm_request_processor is not provided when max_retries is greater than 0.
        """
    async def retrieve(self, query: str, event_emitter: EventEmitter | None = None, prompt_kwargs: dict[str, Any] | None = None, return_query: bool = False) -> pd.DataFrame | tuple[str, pd.DataFrame]:
        """Retrieve data based on the query.

        This method performs a retrieval operation using the configured data store.

        Args:
            query (str): The query string to retrieve documents.
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
            ValueError: If the retrieval process fails after the maximum number of retries.
        """
