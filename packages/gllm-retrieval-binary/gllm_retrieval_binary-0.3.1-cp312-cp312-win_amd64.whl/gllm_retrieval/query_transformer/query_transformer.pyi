import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from gllm_core.schema import Component
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from gllm_inference.output_parser.output_parser import BaseOutputParser as BaseOutputParser
from gllm_inference.prompt_builder.prompt_builder import BasePromptBuilder as BasePromptBuilder
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor
from gllm_inference.request_processor.uses_lm_mixin import UsesLM
from typing import Any, Callable

class BaseQueryTransformer(Component, UsesLM, ABC, metaclass=abc.ABCMeta):
    '''An abstract base class for the query transformers used in Gen AI applications.

    Using the implementations of this class, users can transform a query into a list of strings. Each query transformer
    comes with a default extractor function that extracts the query from the LLM output. Users can also supply their
    own extractor function to customize the extraction process. A JSON extractor function is also provided for
    convenience.

    See the usage examples below for more details.

    Attributes:
        lm_request_processor (LMRequestProcessor | None): The LMRequestProcessor instance to be used for transforming
            queries. Can be None if the transformer does not require an LMRequestProcessor, but it has to be
            supplied.
        extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]]): A function to extract
            the transformed query from the LM output.

    Usage Examples:
        # Using the original constructor
        transformer = ConcreteQueryTransformer(lm_request_processor=None)

        # Using the from_lm_components constructor with a custom JSON extractor
        transformer = ConcreteQueryTransformer.from_lm_components(
            prompt_builder,
            lm_invoker,
            output_parser,
            extract_func=BaseQueryTransformer.json_extractor("query")
        )
    '''
    lm_request_processor: Incomplete
    extract_func: Incomplete
    def __init__(self, lm_request_processor: LMRequestProcessor | None, extract_func: Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]] = None) -> None:
        """Initialize the BaseQueryTransformer.

        Args:
            lm_request_processor (LMRequestProcessor | None): The LMRequestProcessor instance to be used for
                transforming queries. Can be None if the transformer does not require an LMRequestProcessor, but it
                has to be supplied.
            extract_func (Callable[[str | list[str] | dict[str, str | list[str]]], str | list[str]], optional): A
                function to extract the transformed query from the output. Defaults to None, in which case a default
                extractor will be used.
        """
    @abstractmethod
    async def transform(self, query: str | list[str] | dict[str, str | list[str]]) -> list[str]:
        """Transforms the given query into a list of strings.

        This abstract method must be implemented by subclasses to define how the input query is transformed. It is
        expected to return a list of transformed query strings.

        Args:
            query (str | list[str] | dict[str, str | list[str]]): The query, list of queries, or dictionary of queries
                to be transformed.

        Returns:
            list[str]: A list of transformed query strings.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
    @staticmethod
    def json_extractor(key: str) -> Callable[[dict[str, Any]], str | list[str]]:
        """Creates a JSON extractor function for a given key.

        Args:
            key (str): The key to extract from the JSON result.

        Returns:
            Callable[[dict[str, Any]], str | list[str]]: A function that extracts the specified key from a JSON object.

        Raises:
            KeyError: If the specified key is not found in the JSON object.
        """
