from _typeshed import Incomplete
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor
from gllm_retrieval.query_transformer import OneToOneQueryTransformer as OneToOneQueryTransformer
from gllm_retrieval.utils.sql_utils import format_sql_query as format_sql_query, validate_query as validate_query
from typing import Callable

logger: Incomplete
DEFAULT_SYSTEM_PROMPT: str
DEFAULT_RETRY_SYSTEM_PROMPT: str

class TextToSQLQueryTransformer(OneToOneQueryTransformer):
    '''A query transformer that takes one query and outputs exactly one transformed SQL query.

    Attributes:
        lm_request_processor (LMRequestProcessor): The LMRequestProcessor instance to be used for transforming queries.
            The input type determines the prompt builder\'s structure:
            - For strings or lists, it must only have the "query" key;
            - For dictionaries, the keys must match the input.
        extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str]): A function to extract the
            transformed query from the LM output.
        dialect (str): The SQL dialect to be used for formatting and validating the SQL query.
            Please refer to the SQLGlot documentation for supported dialects:
            https://sqlglot.com/sqlglot/dialects/dialect.html
        retry_lm_request_processor (LMRequestProcessor | None): The LMRequestProcessor instance to be used for
            modifying a failed query. If not None, will modify the query upon failure.
        retry_extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]]): A function to
            extract the modified retry query from the LM output.
        max_retries (int): The maximum number of retries for the generation process.
        retry_params (list[str] | None): Parameters for the retry request processor.
    '''
    max_retries: Incomplete
    dialect: Incomplete
    retry_lm_request_processor: Incomplete
    retry_extract_func: Incomplete
    retry_params: Incomplete
    def __init__(self, lm_request_processor: LMRequestProcessor | None, extract_func: Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]] = None, dialect: str = 'postgres', retry_lm_request_processor: LMRequestProcessor | None = None, retry_extract_func: Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]] = None, max_retries: int = 0, retry_params: list[str] | None = None) -> None:
        '''Initialize the TextToSQLQueryTransformer.

        Args:
            lm_request_processor (LMRequestProcessor | None): The LMRequestProcessor instance to be used for
                transforming queries. Can be None if the transformer does not require an LMRequestProcessor, but it
                has to be supplied.
            extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]], optional): A
                function to extract the transformed query from the output. Defaults to None, in which case a default
                extractor will be used.
            dialect (str, optional): The SQL dialect to be used for formatting and validating the SQL query.
                Defaults to "postgres". Please refer to the SQLGlot documentation for supported dialects:
                https://sqlglot.com/sqlglot/dialects/dialect.html.
            retry_lm_request_processor (LMRequestProcessor | None, optional): The LMRequestProcessor instance to be used
                for modifying a failed query. If provided and the max_retries is greater than 0, will modify the query
                upon failure.
            retry_extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]], optional): A
                function to extract the transformed retry query from the output. Defaults to None, in which case a
                default extractor will be used.
            max_retries (int, optional): The maximum number of retries for the generation process. Defaults to 0.
            retry_params (list[str] | None, optional): Parameters for the retry request processor. Defaults to None.

        Raises:
            ValueError: If retry_lm_request_processor is not provided when max_retries is greater than 0.
        '''
    async def transform(self, query: str | list[str] | dict[str, str | list[str]]) -> list[str]:
        '''Transform the input query into exactly one output SQL query.

        The transformer will first call the one-to-one query transformer to transform the input queries into a single
        SQL query. Then, it will format and validate the SQL query before returning it.

        If the SQL query fails validation, it will attempt to modify the query using the retry_lm_request_processor and
        retry the transformation. The number of retries is determined by the `max_retries` attribute.

        Args:
            query (str | list[str] | dict[str, str]): The input query to be transformed.
                If a string is provided, it will be wrapped in a dictionary with "query" key.
                If a list is provided, each query will be processed separately.
                If a dictionary is provided, it will be passed directly to the request processor and the retry
                    request processor.

        Returns:
            list[str]: A list containing the transformed SQL query.

        Raises:
            ValueError: If the query is not a valid sql query after all retries or if the extraction fails.
        '''
