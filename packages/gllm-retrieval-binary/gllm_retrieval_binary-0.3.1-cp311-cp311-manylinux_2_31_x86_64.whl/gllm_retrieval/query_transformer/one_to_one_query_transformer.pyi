from gllm_retrieval.query_transformer.query_transformer import BaseQueryTransformer as BaseQueryTransformer

class OneToOneQueryTransformer(BaseQueryTransformer):
    '''A query transformer that takes one query and outputs exactly one transformed query.

    Attributes:
        lm_request_processor (LMRequestProcessor): The LMRequestProcessor instance to be used for transforming queries.
            The input type determines the prompt builder\'s structure:
            - For strings or lists, it must only have the "query" key;
            - For dictionaries, the keys must match the input.
        extract_func (Callable[[str | list[str] | dict[str, str]], str]): A function to extract the transformed query
            from the LM output.
    '''
    async def transform(self, query: str | list[str] | dict[str, str]) -> list[str]:
        '''Transform the input query into exactly one output query.

        Args:
            query (str | list[str] | dict[str, str]): The input query to be transformed.
                If a string is provided, it will be wrapped in a dictionary with "query" key.
                If a list is provided, each query will be processed separately.
                If a dictionary is provided, it will be passed directly to the request processor.

        Returns:
            list[str]: A list containing the transformed query.
        '''
