from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from gllm_rag.preset.initializer.model_id import ModelId as ModelId, ModelProvider as ModelProvider
from typing import Any

PROVIDER_TO_LM_INVOKER_MAP: dict[str, type[BaseLMInvoker]]

def build_lm_invoker(model_id: str | ModelId, credentials: str | None = None, config: dict[str, Any] | None = None) -> BaseLMInvoker:
    '''Build a language model invoker based on the model identifier and configuration.

    Args:
        model_id (str | ModelId): The model identifier, can either be a ModelId instance or
            a string in the following format:
            1. For TGI: `tgi/base64-encoded-url`
            2. For VLLM: `vllm/model-name@base64-encoded-url`
            3. For cloud providers: `provider/model-name[-version]`
        credentials (str | None, optional): The credentials for the language model. Can either be an API key or
            a path to a credentials file. Defaults to None.
        config (dict[str, Any] | None, optional): Configuration for the language model.
            Defaults to None.

    Returns:
        BaseLMInvoker: An initialized language model invoker.

    Raises:
        ValueError: If the model name is invalid for the provider.

    Examples:
        # Using Anthropic LM invoker
        ```python
        lm_invoker = build_lm_invoker(
            model_id="anthropic/claude-3-5-sonnet-latest",
            credentials="your_anthropic_api_key",
        )
        ```

        # Using Google Generative AI LM invoker
        ```python
        lm_invoker = build_lm_invoker(
            model_id="google-genai/gemini-1.5-pro-latest",
            credentials="your_google_genai_api_key",
        )
        ```

        # Using Google Vertex AI LM invoker
        ```python
        lm_invoker = build_lm_invoker(
            model_id="google-vertexai/gemini-1.5-flash-latest",
            credentials="your_google_vertexai_credentials_path",
        )
        ```

        # Using OpenAI LM invoker
        ```python
        lm_invoker = build_lm_invoker(
            model_id="openai/gpt-4o-mini",
            credentials="your_openai_api_key",
        )
        ```

        # Using OpenAI Compatible LM invoker (DeepInfra, DeepSeek, Groq, TogetherAI)
        ```python
        lm_invoker = build_lm_invoker(
            model_id="groq/llama-3.2-1b-preview",
            credentials="your_groq_api_key",
            config={"base_url": "your_base_url"},
        )
        ```

        # Using VLLM LM invoker
        ```python
        lm_invoker = build_lm_invoker(
            model_id="vllm/llama-3.2-1b-preview@your_base64_encoded_url",
            credentials="your_vllm_api_key",
        )

        # Using TGI LM invoker
        ```python
        lm_invoker = build_lm_invoker(
            model_id="tgi/your_base64_encoded_url",
            credentials="your_tgi_api_key",
        )
        ```
    '''
