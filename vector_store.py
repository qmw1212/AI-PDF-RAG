"""向量存储和检索模块"""
import os
from typing import List
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# 设置HuggingFace镜像源
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'


class VectorStore:
    def __init__(self, collection_name: str = "pdf_documents"):
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        self.collection_name = collection_name
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        try:
            self.collection = self.client.get_collection(name=collection_name)
        except:
            self.collection = self.client.create_collection(name=collection_name)

    def add_documents(self, chunks: List[str]):
        """将文本块添加到向量数据库"""
        embeddings = self.embedding_model.encode(chunks).tolist()

        ids = [f"chunk_{i}" for i in range(len(chunks))]

        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=ids
        )

    def search(self, query: str, n_results: int = 3) -> List[str]:
        """检索与查询最相关的文本块"""
        query_embedding = self.embedding_model.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        return results['documents'][0] if results['documents'] else []

    def reset(self):
        """清空向量数据库"""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(name=self.collection_name)
