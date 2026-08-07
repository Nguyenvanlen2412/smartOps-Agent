from langchain_core.tools import tool
from rag.qa_chain import create_qa_chain

_qa_chain = None


def _get_qa_chain():
    global _qa_chain
    if _qa_chain is None:
        _qa_chain = create_qa_chain()
    return _qa_chain


@tool("search_company_policy_and_db")
def rag_tool(query: str) -> str:
    """Use this tool to search for company policies related to refunds policy, returns, shipping, warranty, FQA, or any other policy."""
    try:
        chain = _get_qa_chain()
        response = chain.invoke({"input": query})
        answer = response.get("answer", "No answer found.")
        source_docs = response.get("context", [])
        context_string = "\n\n".join(
            [f"Source {i+1}:\n{doc.page_content}" for i, doc in enumerate(source_docs)]
        )
        return f"Answer:\n{answer}\n\nSource Documents:\n{context_string}"
    except Exception as e:
        return f"An error occurred while processing your request: {str(e)}"