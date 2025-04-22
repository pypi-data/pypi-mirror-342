from _typeshed import Incomplete
from gllm_core.event import EventEmitter
from gllm_core.schema import Chunk as Chunk
from gllm_pipeline.pipeline import Pipeline
from gllm_rag.preset.initializer import ModelId as ModelId, build_data_store as build_data_store, build_em_invoker as build_em_invoker, build_lm_invoker as build_lm_invoker
from gllm_rag.preset.pipeline_preset import BasePipelinePreset as BasePipelinePreset
from typing import Any, TypedDict

class SimpleRAGState(TypedDict):
    """State schema for the SimpleRAG pipeline.

    Attributes:
        query (str): The input query.
        chunks (list[Chunk]): The retrieved chunks.
        context (str): The repacked context.
        response_synthesis_bundle (dict[str, str]): The bundle containing context for response synthesis.
        response (str): The final response.
        event_emitter (EventEmitter): The event emitter for handling events.
    """
    query: str
    chunks: list[Chunk]
    context: str
    response_synthesis_bundle: dict[str, str]
    response: str
    event_emitter: EventEmitter

class SimpleRAG(BasePipelinePreset):
    '''A simple RAG pipeline preset.

    This preset implements a basic RAG pipeline with the following steps:
    1. Retrieve relevant chunks using BasicRetriever
    2. Repack the chunks into a context
    3. Bundle the context for response synthesis
    4. Generate a response using StuffResponseSynthesizer

    Attributes:
        language_model_id (str | ModelId, optional): The model identifier, must be a string in the following format:
            1. For TGI: `tgi/base64-encoded-url`
            2. For VLLM: `vllm/model-name@base64-encoded-url`
            3. For cloud providers: `provider/model-name[-version]`
            Defaults to "openai/gpt-4o-mini".
        language_model_credentials (str, optional): The credentials for the language model. Defaults to None.
        system_instruction (str, optional): The system instruction for the language model. Defaults to None.
        embedding_model_id (str, optional): The embedding model to use. Defaults to "openai/text-embedding-3-small".
        embedding_model_credentials (str, optional): The credentials for the embedding model. Defaults to None.
        data_store_type (str, optional): The type of data store to use. Defaults to "chroma".
        data_store_index (str, optional): The index name for the data store. Defaults to "default".
        data_store_host (str, optional): The host for the data store. Defaults to None.
        data_store_port (int, optional): The port for the data store. Defaults to None.
        data_store_config (dict, optional): The configuration for the data store. Defaults to None, in which case
            a default configuration for persistent ChromaDB client will be used.

    Example:
    ```python
    rag = SimpleRAG(
        language_model_id="openai/gpt-4o-mini",
        language_model_credentials="test-api-key",
        embedding_model_id="openai/text-embedding-3-small",
        embedding_model_credentials="test-embedding-api-key",
        data_store_type="chroma",
        data_store_index="default",
        data_store_config={"client_type": "persistent", "persist_directory": "./chroma_db"},
    )

    rag("What is the capital of France?")
    ```
    '''
    embedding_model: Incomplete
    embedding_model_credentials: Incomplete
    data_store_type: Incomplete
    data_store_index: Incomplete
    data_store_host: Incomplete
    data_store_port: Incomplete
    data_store_config: Incomplete
    def __init__(self, language_model_id: str | ModelId = 'openai/gpt-4o-mini', language_model_credentials: str | None = None, system_instruction: str | None = None, embedding_model_id: str = 'openai/text-embedding-3-small', embedding_model_credentials: str | None = None, data_store_type: str = 'chroma', data_store_index: str = 'default', data_store_host: str | None = None, data_store_port: int | None = None, data_store_config: dict | None = None) -> None:
        '''Initialize a new SimpleRAG preset.

        Args:
            language_model_id (str | ModelId, optional): The model identifier, must be a string in the following
            format:
                1. For TGI: `tgi/base64-encoded-url`
                2. For VLLM: `vllm/model-name@base64-encoded-url`
                3. For cloud providers: `provider/model-name[-version]`
                Defaults to "openai/gpt-4o-mini".
            language_model_credentials (str | None, optional): The credentials for the language model. Defaults to None.
            system_instruction (str | None, optional): The system instruction for the language model. Defaults to None.
            embedding_model_id (str, optional): The embedding model to use. Defaults to "openai/text-embedding-3-small".
            embedding_model_credentials (str | None, optional): The credentials for the embedding model.
                Defaults to None.
            data_store_type (str, optional): The type of data store to use. Defaults to "chroma".
            data_store_index (str, optional): The index name for the data store. Defaults to "default".
            data_store_host (str | None, optional): The host for the data store. Defaults to None.
            data_store_port (int | None, optional): The port for the data store. Defaults to None.
            data_store_config (dict, optional): The configuration for the data store. Defaults to None, in which case
                a default configuration for the selected data store type will be used.
        '''
    def build(self) -> Pipeline:
        """Build the pipeline.

        Returns:
            Pipeline: The built pipeline.
        """
    def build_initial_state(self, query: str, attachments: list[Any] | None = None, config: dict[str, Any] | None = None) -> dict[str, Any]:
        """Build the initial state for the pipeline.

        Args:
            query (str): The input query.
            attachments (list[Any] | None, optional): The attachments. Defaults to None.
            config (dict[str, Any] | None, optional): The configuration. Defaults to None.

        Returns:
            dict[str, Any]: The initial state for the pipeline.
        """
    def build_config(self, query: str, attachments: list[Any] | None = None, config: dict[str, Any] | None = None) -> dict[str, Any]:
        """Build the runtime configuration for the pipeline.

        Args:
            query (str): The input query.
            attachments (list[Any] | None, optional): The attachments. Defaults to None.
            config (dict[str, Any] | None, optional): The configuration. Defaults to None.

        Returns:
            dict[str, Any]: The runtime configuration for the pipeline.
        """
