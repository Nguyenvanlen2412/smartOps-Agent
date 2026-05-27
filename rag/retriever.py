from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()  # Ensure any necessary environment variables are loaded

def create_retriever():
    embedding_function = HuggingFaceEmbeddings(
        model_name="BAAI/bge-large-en-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True, "batch_size": 32}
    )

    vector_store = Chroma(
        collection_name="my_collection",
        embedding_function=embedding_function,
        persist_directory="./chroma_db"
    )
    print("Vector store initialized and ready for use.")

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3})
    print("Retriever created from the vector store with search parameters: k=3")
    return retriever