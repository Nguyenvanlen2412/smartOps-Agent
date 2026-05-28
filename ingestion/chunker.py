from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
    
def text_splitter(page_content: str):
    headers_to_split_on = [
        ("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")
    ] 
    
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=True)
    markdown_header_splits = markdown_splitter.split_text(page_content) # Returns list of Documents

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    
    # Use split_documents instead of split_text since markdown_header_splits contains Documents
    final_chunks = text_splitter.split_documents(markdown_header_splits)
    
    return final_chunks