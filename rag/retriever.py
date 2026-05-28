from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()


class ChromaRetriever:
    """Configurable retriever backed by a Chroma vector store."""

    DEFAULT_MODEL = "BAAI/bge-large-en-v1.5"
    DEFAULT_COLLECTION = "my_collection"
    DEFAULT_PERSIST_DIR = "./chroma_db"
    DEFAULT_K = 3

    def __init__(
        self,
        model_name: str = None,
        collection_name: str = None,
        persist_directory: str = None,
        device: str = "cpu",
        k: int = None,
    ):
        self.model_name = model_name or self.DEFAULT_MODEL
        self.collection_name = collection_name or self.DEFAULT_COLLECTION
        self.persist_directory = persist_directory or self.DEFAULT_PERSIST_DIR
        self.device = device
        self.k = k or self.DEFAULT_K

        self._embedding_function = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
        )
        self._vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self._embedding_function,
            persist_directory=self.persist_directory,
        )
        print(f"Vector store initialized: collection={self.collection_name}")

    def as_retriever(self):
        """Return a LangChain retriever interface."""
        retriever = self._vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self.k},
        )
        print(f"Retriever created with k={self.k}")
        return retriever


# Backward-compatible factory function
def create_retriever():
    return ChromaRetriever().as_retriever()