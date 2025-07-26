from app.services.embedding import EmbeddingService
from langchain_community.vectorstores import Qdrant
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import openai

class ChatbotService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.vectorstore = Qdrant(
            client=embedding_service.client,
            collection_name=embedding_service.collection_name,
            embeddings=OpenAIEmbeddings(openai_api_key=embedding_service.api_key)
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    async def answer(self, user_message: str) -> str:
        # 1. Qdrant에서 유사 문서 검색
        contexts = await self.embedding_service.search(user_message)
        context_text = "\n".join(contexts)
        print(context_text)

        # 1. System message (role and strict context instruction)
        system_message = (
            "You are a helpful Korean AI assistant. Answer ONLY using the information provided in the [CONTEXT] section below. "
            "If the answer is not in the context, do NOT use any prior knowledge or make up information. "
            "If you do not know the answer based on the context, reply exactly: '정보가 부족하여 답변할 수 없습니다.'"
        )
        # 2. Prompt construction
        prompt = f"""
        [CONTEXT]
        {context_text}

        [QUESTION]
        {user_message}

        Instructions:
        - Use ONLY the information in [CONTEXT] to answer the question.
        - Do NOT use any outside knowledge or make assumptions.
        - Answer in Korean.
        """

        # 3. GPT-4o 호출
        client = openai.AsyncOpenAI(api_key=self.embedding_service.api_key)
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content" : system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()