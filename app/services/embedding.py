from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from app.core.config import settings
import numpy as np
import openai

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

async def openai_embedding(text: str, api_key: str) -> list[float]:
    client = openai.AsyncOpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


class EmbeddingService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        # 메모리 기반 Qdrant 인스턴스
        self.client = QdrantClient(":memory:")
        self.collection_name = "my_embeddings"
        # 컬렉션 생성 (없으면)
        if self.collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config={"size": 1536, "distance": "Cosine"}
            )

    def add_embedding(self, text: str):
        chunks = chunk_text(text)
        for chunk in chunks:
            vector = openai_embedding(chunk, self.api_key)
            point = PointStruct(id=None, vector=vector, payload={"text": text})
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
        return True