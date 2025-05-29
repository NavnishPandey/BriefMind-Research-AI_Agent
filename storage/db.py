
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import yaml
import os

class LocalStorage:
    def __init__(self):
        # Load config
        with open("/teamspace/studios/this_studio/Geo-Aware-Rag_System-for-Travelers/config.yaml", "r") as f:
            config = yaml.safe_load(f)

        self.persist_directory = config.get("vector_db_path", "./storage/chroma_persist")
        os.makedirs(self.persist_directory, exist_ok=True)

        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Initialize the vector store
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def add_summary(self, item):
        title = item["title"]
        summary = item["summary"]
        text = title + "\n" + summary

        doc = Document(page_content=text, metadata={"title": title})
        self.vectorstore.add_documents([doc])
        self.vectorstore.persist()

    def is_duplicate(self, title, threshold=0.85):
        results = self.vectorstore.similarity_search_with_score(title, k=1)
        if results:
            _, score = results[0]
            # Lower score = more similar in Chroma via LangChain
            if score < (1 - threshold):
                return True
        return False

    def persist(self):
        self.vectorstore.persist()
