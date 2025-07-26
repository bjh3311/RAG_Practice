from fastapi import APIRouter, Depends
from app.schemas.chatbot import ChatRequestSchema, ChatResponseSchema, EmbeddingRequestSchema
from app.core.dependencies import get_chatbot_service, get_multi_turn_chatbot_service
from app.services.embedding import EmbeddingService
from app.services.chatbot import ChatbotService

router = APIRouter(prefix="/chatbot",tags=["chatbot"])


@router.post("/basic")
async def chatbot(
    request: ChatRequestSchema,
    chatbot_service: ChatbotService = Depends(get_chatbot_service)
):
    answer = await chatbot_service.answer(request.message)
    return ChatResponseSchema(message=answer) 

@router.post("/multi-turn")
async def chatbot(
    request: ChatRequestSchema,
    multi_turn_service: ChatbotService = Depends(get_multi_turn_chatbot_service)
):
    answer = await multi_turn_service.answer(request.message)
    return ChatResponseSchema(message=answer) 


