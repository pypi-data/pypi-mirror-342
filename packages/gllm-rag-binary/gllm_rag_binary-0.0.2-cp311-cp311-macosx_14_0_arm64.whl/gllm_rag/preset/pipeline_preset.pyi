import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from gllm_pipeline.pipeline import Pipeline as Pipeline
from gllm_rag.preset.initializer import ModelId as ModelId
from typing import Any

class BasePipelinePreset(ABC, metaclass=abc.ABCMeta):
    """Base class for pipeline presets.

    This class functions both as a preset configuration and as an executable pipeline.

    Attributes:
        language_model_id (str | ModelId): The model identifier, can either be a ModelId instance or
            a string in the following format:
            1. For TGI: `tgi/base64-encoded-url`
            2. For VLLM: `vllm/model-name@base64-encoded-url`
            3. For cloud providers: `provider/model-name[-version]`
        language_model_credentials (str | None): The credentials for the language model. Can either be an
            API key or a path to a credentials file.
        system_instruction (str): The system instruction for the language model.
    """
    language_model_id: Incomplete
    language_model_credentials: Incomplete
    system_instruction: Incomplete
    def __init__(self, language_model_id: str | ModelId = 'openai/gpt-4o-mini', language_model_credentials: str | None = None, system_instruction: str | None = None) -> None:
        '''Initialize a new preset.

        Args:
            language_model_id (str | ModelId, optional): The model identifier, can either be a ModelId instance or
                a string in the following format:
                1. For TGI: `tgi/base64-encoded-url`
                2. For VLLM: `vllm/model-name@base64-encoded-url`
                3. For cloud providers: `provider/model-name[-version]`
                Defaults to "openai/gpt-4o-mini".
            language_model_credentials (str, optional): The credentials for the language model. Can either be an
                API key or a path to a credentials file. Defaults to None.
            system_instruction (str): The system instruction for the language model.
        '''
    @abstractmethod
    def build(self) -> Pipeline:
        """Build the pipeline.

        This method must be implemented by subclasses.

        Returns:
            Pipeline: The built pipeline.

        Raises:
            NotImplementedError: If the method is not implemented by subclasses.
        """
    @abstractmethod
    def build_initial_state(self, query: str, attachments: list[Any] | None = None, config: dict[str, Any] | None = None) -> dict[str, Any]:
        """Build the initial state for the pipeline.

        This method must be implemented by subclasses.

        Args:
            query (str): The query to pass to the language model.
            attachments (list[Any] | None, optional): The attachments to pass to the language model. Defaults to None.
            config (dict[str, Any] | None, optional): The configuration to pass to the language model. Defaults to None.

        Returns:
            dict[str, Any]: The initial state for the pipeline.
        """
    @abstractmethod
    def build_config(self, query: str, attachments: list[Any] | None = None, config: dict[str, Any] | None = None) -> dict[str, Any]:
        """Build the runtime configuration for the pipeline.

        This method must be implemented by subclasses.

        Args:
            query (str): The query to pass to the language model.
            attachments (list[Any] | None, optional): The attachments to pass to the language model. Defaults to None.
            config (dict[str, Any] | None, optional): The configuration to pass to the language model. Defaults to None.

        Returns:
            dict[str, Any]: The runtime configuration for the pipeline.
        """
    async def invoke(self, query: str, attachments: list = None, config: dict[str, Any] = None) -> dict[str, Any]:
        """Invoke the pipeline.

        This method must be implemented by subclasses.

        Args:
            query (str): The query to pass to the language model.
            attachments (list, optional): The attachments to pass to the language model. Defaults to None.
            config (dict[str, Any], optional): The configuration to pass to the language model. Defaults to None.

        Returns:
            dict[str, Any]: The response from the language model.

        Raises:
            NotImplementedError: If the method is not implemented by subclasses.
        """
    def __call__(self, query: str, attachments: list = None, config: dict[str, Any] = None) -> dict[str, Any]:
        """Invoke the pipeline.

        This method works in both synchronous and asynchronous contexts.
        It automatically detects the current context and uses the appropriate approach.

        Args:
            query (str): The query to pass to the language model.
            attachments (list, optional): The attachments to pass to the language model. Defaults to None.
            config (dict[str, Any], optional): The configuration to pass to the language model. Defaults to None.

        Returns:
            dict[str, Any]: The response from the language model.
        """
