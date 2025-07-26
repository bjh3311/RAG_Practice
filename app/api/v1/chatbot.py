from fastapi import APIRouter, Depends
from app.schemas.chatbot import ChatRequestSchema, ChatResponseSchema, EmbeddingRequestSchema
from app.core.dependencies import get_embedding_service, get_chatbot_service
from app.services.embedding import EmbeddingService
from app.services.chatbot import ChatbotService

router = APIRouter(tags=["chatbot"])


@router.post("/chatbot")
async def chatbot(
    request: ChatRequestSchema,
    chatbot_service: ChatbotService = Depends(get_chatbot_service)
):
    answer = await chatbot_service.answer(request.message)
    return ChatResponseSchema(message=answer)


@router.post("/embedding")
async def embed(
    request: EmbeddingRequestSchema,
    embedding_service: EmbeddingService = Depends(get_embedding_service)
):
    await embedding_service.add_embedding(request.text)
    return {"message": "임베딩 완료"}