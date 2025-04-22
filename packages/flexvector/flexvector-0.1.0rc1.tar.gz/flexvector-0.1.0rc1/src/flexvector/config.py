from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class VectorDBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        case_sensitive=True,
        extra='ignore',
        env_file='.env',
    )

    # Chroma - https://docs.trychroma.com/docs/run-chroma/persistent-client
    CHROMA_DB_FILE: Optional[str] = "./data/vectorstores/chroma"
    CHROMA_HTTP_URL: Optional[str] = Field(None, description="URL of a remote Chroma DB server")
    CHROMA_HTTP_PORT: Optional[int] = Field(8000, description="Port of a remote Chroma DB server")
    CHROMA_API_KEY: Optional[str] = Field(None, description="API key for a remove Chroma DB server")

    # Qdrant - https://python-client.qdrant.tech/qdrant_client.qdrant_client
    QDRANT_HTTP_URL: Optional[str] = Field(None, description="URL of a remote QDrant server")
    QDRANT_API_KEY: Optional[str] = Field(None, description="API key for a remove QDrant server")

    # Weaviate
    WEAVIATE_HTTP_URL: Optional[str] = Field(None, description="URL of a remote WEAVIATE server")
    WEAVIATE_API_KEY: Optional[str] = Field(None, description="API key for a remove WEAVIATE server")

    # PG Vector Store - https://github.com/pgvector/pgvector
    PG_VECTOR_CONNECTION: Optional[str] = Field(None,
                                                description="URL of a remote PostgreSQL server with pg_vector extension")

    # Azure AI Search - https://pypi.org/project/azure-search-documents/
    AZURE_SEARCH_ENDPOINT: Optional[str] = Field(None, description="URL of a remote Azure Search endpoint")
    AZURE_SEARCH_ADMIN_KEY: Optional[str] = Field(None, description="Admin API key for Azure Search")
    AZURE_SEARCH_API_KEY: Optional[str] = Field(None, description="API key for Azure Search")

    EMBEDDING_DIMENSION: Optional[int] = Field(512, description="Embedding dimension")

    # Open AI
    OPENAI_API_KEY: Optional[str] = Field(None, description="API key for OpenAI")
    EMBEDDING_MODEL: Optional[str] = Field("text-embedding-3-small", description="Embedding model")

    # Open embeddings
    SENTENCE_TRANSFORMER_MODEL: Optional[str] = Field(None, description="Sentence transformer embedding model")

    # Extras
    # https://docs.tavily.com/documentation/quickstart
    TAVILY_API_KEY: Optional[str] = Field(None,
                                          description="API key for Tavily API used for grounding LLM responses using web results")


settings = VectorDBSettings()
