from gllm_core.event import EventEmitter
from gllm_pipeline.pipeline import Pipeline
from gllm_rag.preset.initializer import ModelId as ModelId, build_lm_invoker as build_lm_invoker
from gllm_rag.preset.pipeline_preset import BasePipelinePreset as BasePipelinePreset
from typing import Any, TypedDict

class LMState(TypedDict):
    """The state of the LM pipeline preset."""
    query: str
    event_emitter: EventEmitter
    response: str

class LM(BasePipelinePreset):
    '''A pipeline preset to perform a simple response generation task.

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

    Example:
        ```python
        lm = LM(language_model_id="openai/gpt-4o-mini", language_model_credentials=OPENAI_API_KEY)
        lm("Name 10 animals that starts with the letter \'A\'")
        ```
    '''
    def __init__(self, language_model_id: str | ModelId = 'openai/gpt-4o-mini', language_model_credentials: str | None = None, system_instruction: str = '') -> None:
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
            system_instruction (str, optional): The system instruction for the language model.
                Defaults to an empty string.
        '''
    def build(self) -> Pipeline:
        """Build the pipeline.

        Build a pipeline that performs simple response generation task.

        Returns:
            Pipeline: The built pipeline.
        """
    def build_initial_state(self, query: str, attachments: list[Any] | None = None, config: dict[str, Any] | None = None) -> dict[str, Any]:
        """Build the initial state for the pipeline.

        Args:
            query (str): The query to pass to the language model.
            attachments (list[Any] | None, optional): The attachments to pass to the language model. Defaults to None.
            config (dict[str, Any] | None, optional): The configuration to pass to the language model. Defaults to None.

        Returns:
            dict[str, Any]: The initial state for the pipeline.
        """
    def build_config(self, query: str, attachments: list[Any] | None = None, config: dict[str, Any] | None = None) -> dict[str, Any]:
        """Build the runtime configuration for the pipeline.

        Args:
            query (str): The query to pass to the language model.
            attachments (list[Any] | None, optional): The attachments to pass to the language model. Defaults to None.
            config (dict[str, Any] | None, optional): The configuration to pass to the language model. Defaults to None.

        Returns:
            dict[str, Any]: The runtime configuration for the pipeline.
        """
