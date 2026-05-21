from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core import Document
class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-large-en-v1.5"):
        self.model_name = model_name
        self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)

    def embed(self, documents: list[Document]) -> list[Document]:
        for doc in documents:
            doc.metadata["embedding"] = self.embeddings.embed_query(doc.page_content)
        return documents