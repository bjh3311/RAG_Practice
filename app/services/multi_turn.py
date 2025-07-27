from app.services.embedding import EmbeddingService
from langchain_community.vectorstores import Qdrant
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferMemory
import yaml
from pathlib import Path

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "multi_turn.yaml"

def load_prompt():
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)

class MultiTurnChatbotService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.prompt_config = load_prompt()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt_config["system_message"]),
            ("user", self.prompt_config["user_prompt"])
        ])
        
        # LangChain 방식으로 Qdrant 벡터스토어 설정
        self.vectorstore = Qdrant(
            client=embedding_service.client,
            collection_name=embedding_service.collection_name,
            embeddings=OpenAIEmbeddings(openai_api_key=embedding_service.api_key)
        )

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        self.llm = ChatOpenAI(
            openai_api_key=embedding_service.api_key,
            model="gpt-4o",
            temperature=0.1
        )
 
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.rag_chain = (
            {
                "context": self.retriever | self.format_docs,
                "question": RunnablePassthrough(),
                "chat_history": RunnableLambda(lambda _: self.get_chat_history)
            }
            | self.prompt
            | self.llm
            | StrOutputParser() # 단순 문자열 출력
        )

    @staticmethod
    def format_docs(docs):
        return "\n---\n".join([doc.page_content for doc in docs])
    
    def get_chat_history(self):
        messages = self.memory.chat_history.messages
        if not messages:
            return ""
        history = []
        for i in range(0, len(messages), 2):
            user = messages[i].content if i < len(messages) else ""
            ai = messages[i+1].content if i+1 < len(messages) else ""
            history.append(f"User: {user}\nAI: {ai}")
        return "\n".join(history)
    
    async def answer(self, user_message: str) -> str:
        result = await self.rag_chain.ainvoke(user_message) # 비동기 처리 
        self.memory.chat_memory.add_user_message(user_message)
        self.memory.chat_memory.add_ai_message(result)
        self.print_chat_memory()
        return result
    
    def print_chat_memory(self):
        """chat_memory의 Message 객체를 날 것 그대로 출력합니다."""
        messages = self.memory.chat_memory.messages
        for msg in messages:
            print(msg)  # 또는 print(repr(msg))