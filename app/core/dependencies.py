from functools import lru_cache
from app.services.embedding import EmbeddingService
from app.services.chatbot import ChatbotService
from app.services.multi_turn import MultiTurnChatbotService
from app.services.mcp import MCPService
from app.core.config import settings
from fastapi import Depends


@lru_cache()
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(settings.OPENAI_API_KEY)


@lru_cache()
def get_chatbot_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> ChatbotService:
    return ChatbotService(embedding_service)

@lru_cache()  # 추가
def get_multi_turn_chatbot_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> MultiTurnChatbotService:
    return MultiTurnChatbotService(embedding_service)

@lru_cache()
def get_mcp_service() -> MCPService:
    return MCPService()