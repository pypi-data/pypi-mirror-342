from gllm_inference.em_invoker.em_invoker import BaseEMInvoker as BaseEMInvoker
from gllm_rag.preset.initializer.model_id import ModelId as ModelId, ModelProvider as ModelProvider
from typing import Any

PROVIDER_TO_EM_INVOKER_MAP: dict[str, type[BaseEMInvoker]]

def build_em_invoker(model_id: str | ModelId, credentials: str | None = None, config: dict[str, Any] | None = None) -> BaseEMInvoker:
    '''Build an embedding model invoker based on the specified model name and configuration.

    Args:
        model_id (str | ModelId): Model id either as a ModelId or string in following format:
            1. For TEI: `tei/base64-encoded-url`
            2. For VLLM: `provider/model-name@base64-encoded-url`
            3. For cloud providers: `provider/model-name[-version]`
        credentials (str | None, optional): Path to the credentials file or API key.
            Defaults to None.
        config (dict[str, Any] | None, optional): Configuration for the embedding model.
            Defaults to None.

    Returns:
        BaseEMInvoker: An initialized embedding model invoker.

    Raises:
        ValueError: If the specified model provider is not supported.

    Examples:
        ```
        # Using OpenAI embeddings with API key
        em_invoker = build_em_invoker(
            model_id="openai/text-embedding-ada-002",
            config={"api_key": "your-api-key"}
        )

        # Using OpenAI embeddings with credentials parameter
        em_invoker = build_em_invoker(
            model_id="openai/text-embedding-ada-002",
            credentials="your-api-key"
        )

        # Using Google Generative AI embeddings
        em_invoker = build_em_invoker(
            model_id="google-genai/text-embedding-004",
            config={"api_key": "your-api-key", "task_type": "retrieval_query"}
        )

        # Using Google Vertex AI embeddings
        em_invoker = build_em_invoker(
            model_id="google-vertexai/textembedding-gecko@003",
            credentials="/path/to/credentials.json",
            config={
                "project_id": "your-project-id",
                "location": "us-central1"
            }
        )

        # Using Voyage embeddings
        em_invoker = build_em_invoker(
            model_id="voyage/voyage-embedding-v1",
            credentials="your-api-key"
        )

        # Using TEI embeddings
        em_invoker = build_em_invoker(
            model_id="tei/your-base64-decoded-tei-endpoint",
            config={
                "url": "https://your-tei-endpoint",
                "username": "optional-username",
                "password": "optional-password",
                "query_prefix": "Query: ",
                "document_prefix": "Document: "
            }
        )

        # Using ModelId instance
        from gllm_rag.preset.initializer.model_identifier import ModelId, ModelProvider
        model_id = ModelId(provider=ModelProvider.OPENAI, name="text-embedding-ada-002")
        em_invoker = build_em_invoker(model_id=model_id, config={"api_key": "your-api-key"})

        # Converting to LangChain embeddings
        langchain_embeddings = em_invoker.to_langchain()
        ```
    '''
