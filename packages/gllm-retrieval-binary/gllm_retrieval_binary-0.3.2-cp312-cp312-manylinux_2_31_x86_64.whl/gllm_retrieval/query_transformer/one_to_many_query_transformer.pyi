from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from gllm_inference.output_parser.output_parser import BaseOutputParser as BaseOutputParser
from gllm_inference.prompt_builder.prompt_builder import BasePromptBuilder as BasePromptBuilder
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor
from gllm_retrieval.query_transformer.query_transformer import BaseQueryTransformer as BaseQueryTransformer

class OneToManyQueryTransformer(BaseQueryTransformer):
    '''A query transformer that takes one query and outputs one or more transformed queries.

    When processing multiple input queries, the results from each query are flattened into a single list of
    transformed queries.

    Attributes:
        lm_request_processor (LMRequestProcessor): The LMRequestProcessor instance to be used for transforming queries.
            The input type determines the prompt builder\'s structure:
            - For strings or lists, it must only have the "query" key;
            - For dictionaries, the keys must match the input.
        extract_func (Callable[[str | list[str] | dict[str, str]], list[str]]): A function to extract the list of
            transformed queries from the LM output.
    '''
    async def transform(self, query: str | list[str] | dict[str, str]) -> list[str]:
        '''Transform the input query into one or more output queries.

        Args:
            query (str | list[str] | dict[str, str]): The input query to be transformed.
                If a string is provided, it will be wrapped in a dictionary with "query" key.
                If a list is provided, each query will be processed separately.
                If a dictionary is provided, it will be passed directly to the request processor.

        Returns:
            list[str]: A flattened list of all transformed queries from all input queries.
        '''
