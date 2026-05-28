from langchain_core.tools import BaseTool
from pydantic import Field
from rag.qa_chain import create_qa_chain


class RAGTool(BaseTool):
    """Search company policies and knowledge base using RAG."""

    name: str = "search_company_policy_and_db"
    description: str = (
        "Use this tool to search for company policies related to refunds policy, "
        "returns, shipping, warranty, FQA, or any other policy."
    )

    _qa_chain: object = None  # Lazy-initialized

    @property
    def qa_chain(self):
        """Lazy initialization — only create the chain when first needed."""
        if self._qa_chain is None:
            self._qa_chain = create_qa_chain()
        return self._qa_chain

    def _run(self, query: str) -> str:
        try:
            response = self.qa_chain.invoke({"input": query})
            answer = response.get("answer", "No answer found.")
            source_docs = response.get("context", [])
            context_string = "\n\n".join(
                [f"Source {i+1}:\n{doc.page_content}" for i, doc in enumerate(source_docs)]
            )
            return f"Answer:\n{answer}\n\nSource Documents:\n{context_string}"
        except Exception as e:
            return f"An error occurred while processing your request: {str(e)}"


# Instantiate for use by the agent
rag_tool = RAGTool()