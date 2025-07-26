from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import uuid
import openai

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

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
            print(f"길이: {len(vector)} 일부값: {vector[:5]}")
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector, 
                payload={"text": text})
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
        return True