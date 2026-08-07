from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

from agent.prompt import SYSTEM_PROMPT
from agent.tools.rag_tool import rag_tool
from agent.tools.order_tool import (
    check_order_status_tool,
    list_user_orders_tool,
    cancel_order_tool,
    update_delivery_address_tool,
    request_order_return_tool,
    create_order_tool,
)
from agent.tools.product_tool import search_products_tool, get_product_details_tool
from agent.tools.user_tool import get_user_summary_tool
from agent.tools.ticket_tool import (
    create_ticket_tool,
    list_user_tickets_tool,
    update_ticket_status_tool,
)
from agent.tools.email_tool import send_email_tool
from agent.tools.transaction_tool import check_transaction_status_tool


class SmartOpsAgent:
    """Encapsulates the full agent lifecycle: LLM, tools, memory, and execution."""

    DEFAULT_MODEL = "gemini-3.5-flash-lite"
    DEFAULT_TEMPERATURE = 0.2

    def __init__(self, model: str = None, temperature: float = None):
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature or self.DEFAULT_TEMPERATURE
        self.tools = [
            rag_tool,
            check_order_status_tool,
            list_user_orders_tool,
            cancel_order_tool,
            update_delivery_address_tool,
            request_order_return_tool,
            create_order_tool,
            search_products_tool,
            get_product_details_tool,
            get_user_summary_tool,
            create_ticket_tool,
            list_user_tickets_tool,
            update_ticket_status_tool,
            send_email_tool,
            check_transaction_status_tool,
        ]
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True, output_key="output"
        )
        self._llm = ChatGoogleGenerativeAI(model=self.model, temperature=self.temperature)
        self._executor = self._build_executor()

    def _build_executor(self) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_tool_calling_agent(self._llm, self.tools, prompt)
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            return_intermediate_steps=True,
        )

    def invoke(self, user_input: str) -> str:
        """Send a message to the agent and return the output string."""
        response = self._executor.invoke({"input": user_input})
        output = response.get("output", "")
        if isinstance(output, list):
            texts = []
            for item in output:
                if isinstance(item, dict) and "text" in item:
                    texts.append(item["text"])
                elif isinstance(item, str):
                    texts.append(item)
                else:
                    texts.append(str(item))
            return "\n".join(texts)
        return str(output)

    def reset_memory(self):
        """Clear conversation history."""
        self.memory.clear()


if __name__ == "__main__":
    agent = SmartOpsAgent()
    print(f"SmartOpsAgent initialized with {len(agent.tools)} tools.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the agent. Goodbye!")
            break

        response = agent.invoke(user_input)
        print(f"Agent: {response}")