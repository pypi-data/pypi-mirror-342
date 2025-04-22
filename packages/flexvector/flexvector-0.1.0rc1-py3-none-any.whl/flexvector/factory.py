from flexvector.config import VectorDBSettings
from flexvector.core.models import VectorDBClient


class VectorDBFactory:
    """Factory class for creating vector database clients."""

    @staticmethod
    def chroma(config: VectorDBSettings) -> VectorDBClient:
        """Create a Chroma client."""
        from flexvector.chroma import ChromaClientSync

        return ChromaClientSync(config)

    @staticmethod
    def qdrant(config: VectorDBSettings) -> VectorDBClient:
        """Create a Qdrant client."""
        from flexvector.qdrant import QdrantClient

        return QdrantClient(config)

    @staticmethod
    def weaviate(config: VectorDBSettings) -> VectorDBClient:
        """Create a Weaviate client."""
        from flexvector.weaviate import WeaviateClient

        return WeaviateClient(config)

    @staticmethod
    def pgvector(config: VectorDBSettings) -> VectorDBClient:
        """Create a PGVector client."""
        from flexvector.pgvector import PGVectorClient

        return PGVectorClient(config)

    @staticmethod
    def get(db_type: str, config: VectorDBSettings) -> VectorDBClient:
        """Get a vector database client based on the specified type."""
        factory = VectorDBFactory()
        if db_type == "chroma":
            return factory.chroma(config)
        elif db_type == "qdrant":
            return factory.qdrant(config)
        elif db_type == "weaviate":
            return factory.weaviate(config)
        elif db_type == "pg":
            return factory.pgvector(config)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")