from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import MessagesPlaceholder
from agent.tools.rag_tool import rag_tool
from agent.tools.order_tool import check_order_status_tool
from agent.tools.ticket_tool import create_ticket_tool
from agent.tools.email_tool import send_email_tool
from dotenv import load_dotenv

load_dotenv()  # Ensure any necessary environment variables are loaded
from agent.prompt import SYSTEM_PROMPT


def create_agent():
    print("Initializing the agent creation process.")

    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.2)
    print("LLM initialized with model: gemini-3.1-flash-lite and temperature: 0.2")

    tools = [rag_tool, check_order_status_tool, create_ticket_tool, send_email_tool]
    print(f"Tools initialized: {[tool.name for tool in tools]}")

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="output")
    print("Conversation memory initialized with key: 'chat_history'")

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),  # For conversation history if needed
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")  # For agent's internal reasoning if needed
    ])
    print("System prompt defined for the agent.")

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        return_intermediate_steps=True,  # Set to True if you want to see the agent's thought process and tool calls
    )
    return agent

if __name__ == "__main__":
    agent = create_agent()
    print("Agent created and ready to use.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the agent. Goodbye!")
            break
        response = agent.invoke({"input": user_input})
        print(f"Agent: {response.get('output', '')}")