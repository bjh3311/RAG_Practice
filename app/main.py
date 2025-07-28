from fastapi import FastAPI
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP

app = FastAPI()
app.include_router(api_router)

mcp = FastApiMCP(app)

# Mount the MCP server directly to your FastAPI app
mcp.mount()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 시 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)