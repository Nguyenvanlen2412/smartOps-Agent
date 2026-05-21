from embedder import Embedder
from chunker import Chunker
from loader import FileLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_core import Document

load_dotenv()  # Ensure any necessary environment variables are loaded

class VectorStore:
    def __init__(self, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200, model_name: str = "BAAI/bge-large-en-v1.5"):
        self.file_loader = FileLoader(file_path)
        self.chunker = Chunker(chunk_size, chunk_overlap)
        self.embedder = Embedder(model_name)

    def process(self) -> list[Document]:
        documents = self.file_loader.load()
        chunked_documents = self.chunker.chunk(documents)
        embedded_documents = self.embedder.embed(chunked_documents)
        return embedded_documents
    
if __name__ == "__main__":
    embedder = VectorStore(file_path= [path for path in ["data/techshop_faq.md", "data/techshop_refund_policy.md", "data/techshop_sample_data.md"] if path.endswith(".md")][0])
    processed_documents = embedder.process()
    for doc in processed_documents:
        print(f"Source: {doc.metadata['source']}, Embedding: {doc.metadata['embedding'][:5]}...")

    vector_store = Chroma.from_documents(
        documents=processed_documents,
        embedding=embedder.embeddings
    )
    vector_store.save_local("chroma_vector_store")
    print("Vector store created with", len(vector_store._collection.get_all_ids()), "documents.")