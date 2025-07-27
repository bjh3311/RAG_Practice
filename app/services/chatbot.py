from app.services.embedding import EmbeddingService
from langchain_community.vectorstores import Qdrant
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import openai
import yaml
from pathlib import Path

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "chatbot.yaml"

def load_prompt():
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)

class ChatbotService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.prompt_config = load_prompt()

    async def answer(self, user_message: str) -> str:        # # 1. Qdrant에서 유사 문서 검색
        contexts = await self.embedding_service.search(user_message)
        context_text = "\n".join(contexts)  # 검색된 문서들을 하나의 텍스트로 합침
    
        system_message = self.prompt_config["system_message"]
        prompt = self.prompt_config["user_prompt"].format(
            context=context_text,
            question=user_message
        )
        # 3. GPT-4o 호출
        client = openai.AsyncOpenAI(api_key=self.embedding_service.api_key)
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content" : system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content.strip()