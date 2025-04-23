import abc
from _typeshed import Incomplete
from abc import ABC
from gllm_core.schema import Component
from pydantic import BaseModel, ValidationError as ValidationError
from typing import Any

class BaseRetrievalParameterExtractor(Component, ABC, metaclass=abc.ABCMeta):
    '''An abstract base class for retrieval parameter extractors used in Gen AI apllication.

    This class defines the interface for retrieval parameter extractors, which are responsible
    for extracting retrieval parameters from a given query string.

    The class supports two types of validators:
    1. JSON Schema validator using a dictionary
    2. Pydantic model validator using a BaseModel class

    Example usage with default JSON Schema validator:
        ```python
        from gllm_core.rules import DEFAULT_RETRIEVAL_SCHEMA

        # Initialize extractor with default schema
        extractor = MyExtractor(validator=DEFAULT_RETRIEVAL_SCHEMA)

        # The default schema supports:
        # - Query string
        # - Filters with operations (eq, neq, gt, gte, lt, lte, in, nin, like)
        # - Sort conditions (asc, desc)
        # Example valid parameters:
        {
            "query": "search text",
            "filters": [
                {"field": "category", "operator": "eq", "value": "books"},
                {"field": "price", "operator": "lte", "value": 100}
            ],
            "sort": [
                {"field": "date", "order": "desc"}
            ]
        }
        ```

    Example usage with default Pydantic validator:
        ```python
        from gllm_core.rules import DefaultRetrievalSchema

        # Initialize extractor with default schema
        extractor = MyExtractor(validator=DefaultRetrievalSchema)

        # The default schema supports:
        # - Query string (required)
        # - Optional filter conditions with FilterOperator enum
        # - Optional sort conditions with SortOrder enum
        # Example valid parameters:
        {
            "query": "search text",
            "filters": [
                {
                    "field": "category",
                    "operator": FilterOperator.EQUALS,
                    "value": "books"
                }
            ],
            "sort": [
                {
                    "field": "date",
                    "order": SortOrder.DESCENDING
                }
            ]
        }
        ```

    For custom validation requirements, you can also define your own schemas:

    Example with custom JSON Schema:
        ```python
        # Define custom JSON Schema
        schema = {
            "type": "object",
            "properties": {
                "top_k": {"type": "integer", "minimum": 1},
                "threshold": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": ["top_k", "threshold"]
        }

        # Initialize extractor with custom schema
        extractor = MyExtractor(validator=schema)
        ```

    Example with custom Pydantic model:
        ```python
        from pydantic import BaseModel, Field

        # Define custom Pydantic model
        class SearchParams(BaseModel):
            top_k: int = Field(gt=0)
            threshold: float = Field(ge=0, le=1)

        # Initialize extractor with custom model
        extractor = MyExtractor(validator=SearchParams)
        ```

    The validator will automatically run after parameter extraction to ensure
    the returned parameters meet the specified schema/model requirements.

    Attributes:
        validator (dict | type[BaseModel] | None): The validator to use for validating
            the extracted parameters. Can be either a JSON Schema or a Pydantic model class.
    '''
    validator: Incomplete
    def __init__(self, validator: dict[str, Any] | type[BaseModel] | None = None) -> None:
        """Initializes the BaseRetrievalParameterExtractor object.

        Args:
            validator(dict | type[BaseModel] | None, optional): The validator to use for validating the extracted
                parameters. Can be either a JSON Schema or a Pydantic model class. Defaults to None.

        Raises:
            TypeError: If the validator is not a dict or Pydantic model.
        """
    async def extract_parameters(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Extracts retrieval parameters from the input query.

        This method is a wrapper around the `_extract_parameters` method, which performs the actual parameter
        extraction. It also includes validation of the extracted parameters using the `_validate_parameters` method.

        Args:
            query(str): The input query string.
            **kwargs(Any): Additional keyword arguments to pass to the extractor.

        Returns:
            dict[str, Any]: A dictionary containing the extracted parameters.

        Raises:
            RuntimeError: If an error occurs during the extraction process.
        """
