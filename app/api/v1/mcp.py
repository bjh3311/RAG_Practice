from fastapi import APIRouter, Depends
from app.schemas.mcp import MCPRequestSchema, MCPResponseSchema
from app.services.mcp import MCPService
from app.core.dependencies import get_mcp_service

router = APIRouter(prefix="/mcp",tags=["mcp"])

@router.post("/search")
async def langgraph(
    request: MCPRequestSchema,
    mcp_service: MCPService = Depends(get_mcp_service)
):
    message = await mcp_service.summarize(request.content)
    return MCPResponseSchema(message=message)
    
