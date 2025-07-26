from app.services.embedding import EmbeddingService
import openai

class ChatbotService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service

    async def answer(self, user_message: str) -> str:
        # # 1. Qdrant에서 유사 문서 검색
        # contexts = await self.embedding_service.search(user_message)
        # context_text = "\n".join(contexts)

        # 2. 프롬프트 생성
        prompt = f"""
                        질문: {user_message}
                    """

        # 3. GPT-4o 호출
        client = openai.AsyncOpenAI(api_key=self.embedding_service.api_key)
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "너는 친절한 한국어 AI 비서야."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()