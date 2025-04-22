from _typeshed import Incomplete
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor, UsesLM
from gllm_retrieval.retrieval_parameter_extractor.retrieval_parameter_extractor import BaseRetrievalParameterExtractor as BaseRetrievalParameterExtractor
from pydantic import BaseModel as BaseModel
from typing import Any

class LMBasedRetrievalParameterExtractor(BaseRetrievalParameterExtractor, UsesLM):
    '''A retrieval parameter extractor that uses a language model to extract parameters from a query.

    This class processes input queries and additional parameters through a language model to extract
    structured parameters for retrieval operations.

    Attributes:
        lm_request_processor (LMRequestProcessor): The language model processor for parameter extraction.
        validator (dict[str, Any] | type[BaseModel]): The validator schema or Pydantic model.

    Note:
        The LM request processor\'s prompt template MUST include placeholders for all parameters:
        - The \'query\' parameter is required
        - Any additional parameters passed through kwargs must also have corresponding
          placeholders in the prompt template.

    Example Usage:
        extractor = LMBasedRetrievalParameterExtractor(lm_request_processor)
        params = await extractor.extract_parameters(
            "Find security documentation",
            department="InfoSec",
            content_type="security_policies"
        )

    Example Prompt Template:
        query: {query}
        department: {department}
        content_type: {content_type}

    Example Output:
        {
            "query": "Find security documentation",
            "filters": [
                {
                    "field": "category",
                    "operator": "eq",
                    "value": "security_policies"
                },
                {
                    "field": "department",
                    "operator": "eq",
                    "value": "InfoSec"
                }
            ],
            "sort": [
                {
                    "field": "date",
                    "order": "desc"
                }
            ]
        }
    '''
    lm_request_processor: Incomplete
    def __init__(self, lm_request_processor: LMRequestProcessor, validator: dict[str, Any] | type[BaseModel] | None = None) -> None:
        """Initialize the LMRetrievalParameterExtractor.

        Args:
            lm_request_processor (LMRequestProcessor): The language model processor for parameter extraction.
            validator (dict[str, Any] | type[BaseModel], optional): The validator schema or Pydantic model.
                Defaults to None.
        """
