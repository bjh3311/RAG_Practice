from fastapi import APIRouter, Depends
from app.schemas.chatbot import ChatRequestSchema, ChatResponseSchema, EmbeddingRequestSchema
from app.core.dependencies import get_embedding_service
from app.services.embedding import EmbeddingService

router = APIRouter(tags=["chatbot"])


@router.post("/chatbot", response_model=ChatResponseSchema)
async def chatbot(request: ChatRequestSchema):
    return ChatResponseSchema(message="보고서")


@router.post("/embedding")
async def embed(
    request: EmbeddingRequestSchema,
    embedding_service: EmbeddingService = Depends(get_embedding_service)
):
    await embedding_service.add_embedding(request.text)
    return {"message": "임베딩 완료"}