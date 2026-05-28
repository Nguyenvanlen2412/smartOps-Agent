from rag.retriever import create_retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


class QAChainBuilder:
    """Builds a retrieval-augmented QA chain with configurable LLM and prompt."""

    DEFAULT_MODEL = "gemini-3.1-flash-lite"
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_SYSTEM_PROMPT = (
        "You are a helpful assistant.\n"
        "Use the following retrieved documents to answer the question. "
        "If you don't know the answer, say you don't know.\n\n"
        "Context:\n"
        "{context}"
    )

    def __init__(
        self,
        model: str = None,
        temperature: float = None,
        system_prompt: str = None,
    ):
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature or self.DEFAULT_TEMPERATURE
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT

    def build(self):
        """Construct and return the retrieval QA chain."""
        print("Initializing the QA chain creation process.")

        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "{input}"),
        ])

        llm = ChatGoogleGenerativeAI(
            model=self.model,
            temperature=self.temperature,
        )

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        chain = create_retrieval_chain(
            retriever=create_retriever(),
            combine_docs_chain=question_answer_chain,
        )

        print(f"QA chain created with model={self.model}, temp={self.temperature}")
        return chain


# Backward-compatible factory function
def create_qa_chain():
    return QAChainBuilder().build()