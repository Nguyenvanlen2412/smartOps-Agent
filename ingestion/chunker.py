from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter, TokenTextSplitter
from langchain_core import Document
class Chunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = MarkdownHeaderTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

    def chunk(self, documents: list[Document]) -> list[Document]:
        chunked_documents = []
        for doc in documents:
            chunks = self.text_splitter.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                chunked_documents.append(Document(page_content=chunk, metadata={"source": f"{doc.metadata['source']}_chunk_{i}"}))
        return chunked_documents
    