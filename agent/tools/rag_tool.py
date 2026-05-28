from langchain_core.tools import Tool

from rag.qa_chain import create_qa_chain

_qa_chain = create_qa_chain()
def qa_tool(query: str) -> str:
    """
    Search company policies and return relevant information based on the user's query.
    """
    try:
        response = _qa_chain.invoke({"input": query})
        answer = response.get("answer", "No answer found.")  # Access the generated answer
        source_docs = response.get("context", [])
        context_string = "\n\n".join([f"Source {i+1}:\n{doc.page_content}" for i, doc in enumerate(source_docs)])
        return f"Answer:\n{answer}\n\nSource Documents:\n{context_string}"

    except Exception as e:
        return f"An error occurred while processing your request: {str(e)}"
    
rag_tool = Tool(
    name="search_company_policy_and_db",
    description="Use this tool to search for company policies related to refunds policy, returns, shipping, warranty, FQA, or any other policy.",
    func=qa_tool
)