from retriever import create_retriever
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()  # Ensure any necessary environment variables are loaded
def create_qa_chain():
    print("Initializing the QA chain creation process.")
    prompt_template = """Use the following retrieved documents to answer the question. If you don't know the answer, say you don't know."""
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = RetrievalQA.from_chain_type(
        llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite",
                                    temperature=0.7,
                                    max_tokens=2048),
        retriever=create_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    print("QA chain created with ChatGoogleGenerativeAI and the retriever.")
    return chain