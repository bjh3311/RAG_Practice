from pydantic import BaseModel, Field

class ChatRequestSchema(BaseModel):
    message: str = Field(..., example="보고서를 요약해줘", description="사용자의 챗봇 메시지")

class ChatResponseSchema(BaseModel):
    message: str = Field(..., example="보고서는 내용이 간단합니다", description="LLM 응답")

class EmbeddingRequestSchema(BaseModel):
    text: str = Field(..., example="MSA란 Micro service Archi....", description="임베딩할 본문")