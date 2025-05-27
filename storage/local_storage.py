# research_rag_agent/storage/local_storage.py

import chromadb
from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings


class LocalStorage:
    def __init__(self, persist_directory="chroma_db"):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        self.collection_name = "research_papers"
        self.embedding = HuggingFaceEmbeddings()
        if self.collection_name not in self.client.list_collections():
            self.collection = self.client.create_collection(name=self.collection_name)
        else:
            self.collection = self.client.get_collection(name=self.collection_name)

    def is_duplicate(self, title):
        results = self.collection.query(
            query_texts=[title],
            n_results=1
        )
        return bool(results["documents"][0]) if results["documents"] else False

    def add_summary(self, paper):
        doc_id = paper["url"]
        metadata = {
            "title": paper["title"],
            "url": paper["url"],
            "published": paper["published"]
        }
        self.collection.add(
            documents=[paper["summary"]],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def persist(self):
        self.client.persist()
