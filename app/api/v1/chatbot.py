from fastapi import APIRouter

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/")
async def chatbot_root():
    return {"messages" : "Chatbot v1 root"}