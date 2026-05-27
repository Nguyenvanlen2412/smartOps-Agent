from rag.retriever import create_retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()  # Ensure any necessary environment variables are loaded
def create_qa_chain():
    print("Initializing the QA chain creation process.")
    system_prompt = (
        "You are a helpful assistant.\n"
        "Use the following retrieved documents to answer the question. "
        "If you don't know the answer, say you don't know.\n\n"
        "Context:\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0.7,
    )
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(
        retriever = create_retriever(), 
        combine_docs_chain=question_answer_chain
        )
    print("QA chain created with ChatGoogleGenerativeAI and the retriever.")
    return chain

"""

You are **very close**, and structurally this is exactly how you customize the internal prompt. However, there are two distinct LangChain bugs/deprecated patterns in your code that will either throw an error or cause unexpected behavior when you run it.

Here is what needs fixing, why it matters, and the corrected code.

---

### The Two Things to Fix

#### 1. Missing return_source_documents configuration in chain_type_kwargs

When you set return_source_documents=True on the RetrievalQA chain, the underlying CombineDocumentsChain needs to know how to bundle everything together. Because you are overriding chain_type_kwargs, you explicitly need to tell it which variable in your template represents the input documents.

* **The Fix:** Add "document_variable_name": "context" inside your chain_type_kwargs dictionary. If you leave this out, LangChain will often fail because it can't map your retrieved docs to your {context} variable.

#### 2. The RetrievalQA class is legacy code

While it still works in older environments, RetrievalQA was deprecated by the LangChain team in favor of the more modern, flexible **LCEL (LangChain Expression Language)** chains like create_retrieval_chain.

Since we want to make sure your code runs perfectly without deprecation warnings, it's highly recommended to use the modern syntax.

---

### The Corrected Code (Modern Pattern)

This updated version uses LangChain's recommended modern syntax. It does exactly what your code intends to do, handles the prompt variables correctly, and ensures you get the source_documents back without errors.

```python
from retriever import create_retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()  # Ensure any necessary environment variables are loaded

def create_qa_chain():
    print("Initializing the QA chain creation process.")
    
    # 1. Define the system prompt with strict guardrails
    # Note: Modern LangChain automatically handles mapping the context and input!
    system_prompt = (
        "You are a helpful assistant.\n"
        "Use the following retrieved documents to answer the question. "
        "If you don't know the answer, say you don't know.\n\n"
        "Context:\n"
        "{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"), # Modern chains look for {input} instead of {question}
    ])
    
    # 2. Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite", # Note: ensuring accurate model naming convention
        temperature=0.7,
        max_tokens=2048
    )
    
    # 3. Create the document combination chain (combines prompt + LLM)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    # 4. Create the final retrieval chain (wires the retriever to the QA chain)
    # This automatically handles returning source documents under the 'context' key
    chain = create_retrieval_chain(create_retriever(), question_answer_chain)
    
    print("QA chain created with ChatGoogleGenerativeAI and the retriever.")
    return chain

```

### Quick Note on Invoking the New Chain

Because the modern chain structure maps variables slightly differently, when you call this chain, your input keys change just a bit.

Instead of passing {"query": "your question"}, you pass {"input": "your question"}:

```python
# How to run the new chain
qa_chain = create_qa_chain()
response = qa_chain.invoke({"input": "What is the company remote work policy?"})

# How to access your outputs:
print("Answer:", response["answer"])
print("Source Docs:", response["context"]) # This holds your list of source Documents!

``` """