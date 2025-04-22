from enum import StrEnum
from gllm_datastore.vector_data_store.vector_data_store import BaseVectorDataStore as BaseVectorDataStore
from gllm_inference.em_invoker.em_invoker import BaseEMInvoker
from langchain_core.embeddings import Embeddings
from typing import Any

class DataStoreType(StrEnum):
    """Enum for the supported vector data store types."""
    CHROMA = 'chroma'
    ELASTICSEARCH = 'elasticsearch'

def build_data_store(store_type: str | DataStoreType, index_name: str, embedding: Embeddings | BaseEMInvoker | None = None, host: str | None = None, port: int | None = None, config: dict[str, Any] | None = None) -> BaseVectorDataStore:
    '''Build a vector data store instance based on the specified type and configuration.

    Args:
        store_type (str | DataStoreType): Type of the vector data store to create.
            Can be a string or DataStoreType enum.
        index_name (str): Name of the index or collection to use.
        embedding (Embeddings | BaseEMInvoker | None, optional): The embedding model to use. Defaults to None.
        host (str | None, optional): Host address for the data store. For Chroma and Elasticsearch.
            Defaults to None.
        port (int | None, optional): Port number for the data store. For Chroma and Elasticsearch.
            Defaults to None.
        config (dict[str, Any] | None, optional): Additional configuration parameters for the data store.
            Defaults to None.

    Returns:
        BaseVectorDataStore: An initialized vector data store instance.

    Raises:
        ValueError: If an unsupported data store type is specified.

    Examples:
        ```
        # Using minimal parameters
        store = build_data_store(
            store_type="chroma",
            index_name="my_collection",
            embedding=my_embeddings
        )

        # Using host and port parameters
        store = build_data_store(
            store_type="chroma",
            index_name="my_collection",
            embedding=my_embeddings,
            host="localhost",
            port=8000
        )

        # Using additional configuration
        store = build_data_store(
            store_type=DataStoreType.CHROMA,
            index_name="my_collection",
            embedding=my_embeddings,
            config={"client_type": "persistent", "persist_directory": "/path/to/dir"}
        )

        # Elasticsearch example with host and port
        store = build_data_store(
            store_type=DataStoreType.ELASTICSEARCH,
            index_name="my_index",
            embedding=my_embeddings,
            host="localhost",
            port=9200
        )

        # Elasticsearch example with explicit config
        store = build_data_store(
            store_type=DataStoreType.ELASTICSEARCH,
            index_name="my_index",
            embedding=my_embeddings,
            config={"url": "http://localhost:9200", "user": "elastic"}
        )
        ```
    '''
