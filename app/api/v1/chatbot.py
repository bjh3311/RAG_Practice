from fastapi import APIRouter
from app.schemas.chatbot import ChatRequestSchema, ChatResponseSchema

router = APIRouter(tags=["chatbot"])

@router.post("/chatbot", response_model=ChatResponseSchema)
async def chatbot_root(request: ChatRequestSchema):
    return ChatResponseSchema(message="보고서")