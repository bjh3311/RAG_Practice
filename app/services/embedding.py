from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import numpy as np

def fake_embedding(text: str) -> list[float]:
    # 실제 임베딩 모델 대신 랜덤 벡터 (예시)
    return list(np.random.rand(1536))

class EmbeddingService:
    def __init__(self):
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
        vector = fake_embedding(text)
        point = PointStruct(id=None, vector=vector, payload={"text": text})
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        return True