from fastapi import APIRouter
from app.api.v1.chatbot import router as chatbot_router
from app.api.v1.embedding import router as embedding_router  # 임포트 추가
from app.api.v1.mcp import router as mcp_router


api_router = APIRouter()
api_router.include_router(chatbot_router, prefix="/api/v1")
api_router.include_router(embedding_router, prefix="/api/v1")  
api_router.include_router(mcp_router, prefix="/api/v1") # 라우터 등록