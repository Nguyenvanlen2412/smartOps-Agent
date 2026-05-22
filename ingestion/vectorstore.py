from pathlib import Path
from chunker import text_splitter
from loader import load_file
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_core.documents import Document
load_dotenv()  # Ensure any necessary environment variables are loaded

if __name__ == "__main__":
    # Load documents from a file
    folder_path = Path("./data")
    print(folder_path.exists())
    all_documents = []

    for file in folder_path.glob("*.md"):
        documents = load_file(str(file))
        all_documents.extend(documents)
        print(f"Loaded {len(documents)} documents from {file.name}")
    
    # Split the documents into chunks
    all_chunks = []

    for doc in all_documents:
        chunks = text_splitter(doc.page_content)
        for chunk in chunks:
            chunk.metadata.update(doc.metadata)  # Preserve original metadata
            all_chunks.append(chunk)

    if not all_chunks:
        print("No chunks were created from the documents.")
    else:
        print(f"Created {len(all_chunks)} chunks from the documents.")
        model_kwargs = {
            "device": "cpu" 
        }
        encode_kwargs = {
            "normalize_embeddings": True,
            "batch_size": 32
        }
        model_name = "BAAI/bge-large-en-v1.5"
        # Embed the document chunks
        embedding_function = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
            )
        # Create a vector store and add the embedded documents
        vector_store = Chroma(
            collection_name="my_collection",
            embedding_function=embedding_function,
            persist_directory="./chroma_db"
            )
        vector_store.add_documents(all_chunks)
        print(f"Added {len(all_chunks)} chunks to the vector store.")
