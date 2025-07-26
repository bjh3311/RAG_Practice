from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
import openai

def chunk_text(text, chunk_size=200, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    # LangChain splitter는 문서 리스트를 받으므로, 단일 텍스트는 리스트로 감싸줌
    return splitter.split_text(text)

async def openai_embedding(text: str, api_key: str) -> list[float]:
    client = openai.AsyncOpenAI(api_key=api_key)
    response = await client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


class EmbeddingService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # 메모리 기반 Qdrant 인스턴스
        self.client = QdrantClient(":memory:")
        self.collection_name = "my_embeddings"
        # 컬렉션 생성 (없으면)
        if self.collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config={"size": 1536, "distance": "Cosine"}
            )

    async def add_embedding(self, text: str):
        chunks = chunk_text(text)
        for chunk in chunks:
            vector = await openai_embedding(chunk, self.api_key)
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector, 
                payload={"text": chunk})
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
        return True
    
    async def search(self, user_message: str):
        # user_messgae 임베딩
        query_vector = await openai_embedding(user_message, self.api_key)
        # Qdrant에서 유사한 벡터 검색
        result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=3
        )
        return [hit.payload["text"] for hit in result]
