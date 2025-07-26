from functools import lru_cache
from app.services.embedding import EmbeddingService

@lru_cache()
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()