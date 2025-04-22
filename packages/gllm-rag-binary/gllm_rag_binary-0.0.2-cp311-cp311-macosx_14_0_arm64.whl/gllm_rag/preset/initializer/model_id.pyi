from _typeshed import Incomplete
from enum import StrEnum
from pydantic import BaseModel, HttpUrl
from typing import Annotated

class ModelProvider(StrEnum):
    """Defines the supported model providers."""
    ANTHROPIC = 'anthropic'
    GOOGLE_GENAI = 'google-genai'
    GOOGLE_VERTEXAI = 'google-vertexai'
    OPENAI = 'openai'
    VOYAGE = 'voyage'
    TEI = 'tei'
    TGI = 'tgi'
    DEEPINFRA = 'deepinfra'
    DEEPSEEK = 'deepseek'
    GROQ = 'groq'
    TOGETHER_AI = 'together-ai'
    VLLM = 'vllm'

VALID_ANTHROPIC_MODEL: Incomplete
VALID_GOOGLE_MODEL: Incomplete
VALID_OPENAI_MODEL: Incomplete
VALID_VOYAGE_MODEL: Incomplete
VALID_DEEPINFRA_MODEL: Incomplete
VALID_DEEPSEEK_MODEL: Incomplete
VALID_GROQ_MODEL: Incomplete
VALID_TOGETHER_AI_MODEL: Incomplete
VALID_MODEL_NAME_MAP: Incomplete
DEFAULT_MODEL_VERSION_MAP: Incomplete

def validate_model_name(name: str, provider: ModelProvider) -> str:
    """A Pydantic validator that validates the model name is valid for the given provider.

    This validates that the model name is valid for the given provider by checking the following:
    1. If the provider is TGI or TEI, the model name must be a valid URL.
    2. If the provider is VLLM, the model name must be a valid model name and a valid URL.
    3. If the provider is cloud provider, the model name must be a valid model name for the provider.

    Args:
        name (str): The model name to validate.
        provider (ModelProvider): The provider to validate the model name against.

    Returns:
        str: The validated model name.

    Raises:
        ValueError: If the model name is invalid for the provider.
    """

name_validator: Incomplete
version_validator: Incomplete

class ModelId(BaseModel):
    """Defines a representation of a valid model id.

    Attributes:
        provider (ModelProvider): The provider of the model.
        name (str): The name of the model.
        version (str | None): The version of the model.
        url (HttpUrl | None): The URL for self-hosted models (e.g. TGI, VLLM).

    Raises:
        ValueError: If the model name is invalid for the provider.
    """
    provider: ModelProvider
    name: Annotated[str, name_validator]
    version: Annotated[str | None, version_validator]
    url: HttpUrl | None
    @classmethod
    def from_string(cls, model_id: str) -> ModelId:
        """Parse a model name into a ModelId object.

        The input string must be in a specific format, depending on the provider:
        1. For TGI or TEI: `provider/base64-encoded-url`
        2. For VLLM: `provider/model-name@base64-encoded-url`
        3. For cloud providers: `provider/model-name[-version]`

        Args:
            model_id (str): The model name to parse.

        Returns:
            ModelId: The parsed ModelId object.

        Raises:
            ValueError: If the string format is invalid or the provider is not supported.
        """
    def get_formatted_name(self) -> str:
        """Return a formatted string representation of the model name.

        The format varies by provider:
        1. For TGI or TEI: `base64-encoded-url`
        2. For VLLM: `model-name@base64-encoded-url`
        3. For cloud providers: `model-name[-version]`

        Returns:
            str: The formatted string representation of the model name.

        Raises:
            ValueError: If URL is required but not provided, or if URL is invalid.
        """
    def to_string(self) -> str:
        """Return a formatted string representation of the provider and model name.

        The format varies by provider:
        1. For TGI or TEI: `provider/base64-encoded-url`
        2. For VLLM: `provider/model-name@base64-encoded-url`
        3. For cloud providers: `provider/model-name[-version]`

        Returns:
            str: The formatted string representation of the provider and model name.

        Raises:
            ValueError: If URL is required but not provided, or if URL is invalid.
        """
