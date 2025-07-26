from functools import lru_cache
from app.services.embedding import EmbeddingService
from app.core.config import settings

@lru_cache()
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(settings.OPENAI_API_KEY)