from app.services.embedding import EmbeddingService
from langchain_community.vectorstores import Qdrant
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import yaml
from pathlib import Path

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "chatbot.yaml"

def load_prompt():
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)

class MultiTurnChatbotService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.prompt_config = load_prompt()
        
        # LangChain 방식으로 Qdrant 벡터스토어 설정
        self.vectorstore = Qdrant(
            client=embedding_service.client,
            collection_name=embedding_service.collection_name,
            embeddings=OpenAIEmbeddings(openai_api_key=embedding_service.api_key)
        )
        
        # 검색기 설정
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )
        
        # 대화 메모리 설정
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # LLM 설정
        self.llm = ChatOpenAI(
            openai_api_key=embedding_service.api_key,
            model="gpt-4o",
            temperature=0.1
        )
        
        # 대화형 검색 체인 설정
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            verbose=True
        )

    async def answer(self, user_message: str) -> str:
        # ConversationalRetrievalChain은 이미 비동기를 지원하지 않으므로 동기 호출
        result = self.qa_chain({"question": user_message})
        return result["answer"]