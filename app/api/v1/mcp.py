from fastapi import APIRouter, Depends
from app.schemas.mcp import MCPRequestSchema, MCPResponseSchema
from app.services.mcp import MCPService
from app.core.dependencies import get_mcp_service

router = APIRouter(prefix="/mcp",tags=["mcp"])

@router.post("/langgraph")
async def langgraph(
    request: MCPRequestSchema,
    mcp_service: MCPService = Depends(get_mcp_service)
):
    return MCPResponseSchema(message="abc")
    
