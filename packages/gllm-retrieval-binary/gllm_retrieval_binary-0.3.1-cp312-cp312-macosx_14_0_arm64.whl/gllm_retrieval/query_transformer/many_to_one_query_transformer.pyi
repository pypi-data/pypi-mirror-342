from _typeshed import Incomplete
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor
from gllm_retrieval.query_transformer.query_transformer import BaseQueryTransformer as BaseQueryTransformer
from typing import Callable

class ManyToOneQueryTransformer(BaseQueryTransformer):
    '''A query transformer that takes multiple queries and outputs a single transformed query.

    Attributes:
        lm_request_processor (LMRequestProcessor): The LMRequestProcessor instance to be used for transforming queries.
            The input type determines the prompt builder\'s structure:
            - For strings or lists, it must only have the "query" key;
            - For dictionaries, the keys must match the input.
        extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str]): A function to extract the
            transformed query from the LM output.
        combine_func (Callable[[list[str]], str]): A function to combine multiple queries into a single string.
    '''
    combine_func: Incomplete
    def __init__(self, lm_request_processor: LMRequestProcessor, extract_func: Callable[[str | list[str] | dict[str, str | list[str]]], str] = None, combine_func: Callable[[list[str]], str] = None) -> None:
        """Initialize the ManyToOneTransformer.

        Args:
            lm_request_processor (LMRequestProcessor): The LMRequestProcessor instance to be used for transforming
                queries.
            extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str], optional): A function to
                extract the transformed query from the LM output. Defaults to None, in which case a default extractor
                will be used.
            combine_func (Callable[[list[str]], str], optional): A function to combine multiple queries into a single
                string to pass to the LM. Defaults to None, in which case a default combiner will be used.
        """
    async def transform(self, query: str | list[str] | dict[str, str | list[str]]) -> list[str]:
        '''Transform a list of queries into a single output query.

        The transformer will first look into the input whether it can find a list of queries, either the input itself
        is a list, or the dictionary contains a list of queries. If it finds a list of queries, it will combine them
        into a single query using the `combine_func` attribute. The combined query will then be sent to the LM.
        The output of the LM will be extracted using the `extract_func`.

        Args:
            query (str | list[str] | dict[str, str | list[str]]): The input queries to be transformed.
                If a string or a list of strings is provided, the queries will be wrapped in a dictionary with "query"
                key.
                If a dictionary is provided, list values will be combined using the `combine_func` and the resulting
                dictionary will be sent to the request processor.

        Returns:
            list[str]: A list containing a single transformed query.
        '''
