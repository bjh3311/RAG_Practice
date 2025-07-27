from pydantic import BaseModel, Field

class MCPRequestSchema(BaseModel):
    content: str = Field(
        ...,
        example="네이버 뉴스에서 오늘 IT 기사 3개를 요약해서 Notion에 저장해줘.",
        description="사용자의 자연어 명령"
    )

class MCPResponseSchema(BaseModel):
    message: str = Field(..., description="처리 결과 또는 요약 내용")