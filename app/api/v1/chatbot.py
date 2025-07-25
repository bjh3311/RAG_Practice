from fastapi import APIRouter
from app.schemas.chatbot import ChatRequestSchema, ChatResponseSchema

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/", response_model=ChatResponseSchema)
async def chatbot_root(request: ChatRequestSchema):
    return ChatResponseSchema(message="보고서")