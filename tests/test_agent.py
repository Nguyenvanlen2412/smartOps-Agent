"""End-to-end agent wiring tests.

These prove the SmartOpsAgent orchestration itself -- prompt -> LLM tool-call
decision -> correct tool invoked -> tool result fed back -> final answer --
independent of the real Gemini model or real HTTP backend. The LLM is replaced
with a scripted FakeMessagesListChatModel (each call returns the next canned
AIMessage), and individual tool `_run` methods are monkeypatched so no network
call happens. Tool *behavior* (HTTP contract, error handling) is covered
separately in test_tools.py and test_mock_api_integration.py; this file only
verifies the agent picks the right tool with the right arguments and produces
the model's final answer.
"""

from unittest.mock import patch

from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage

from agent.agent import SmartOpsAgent
from agent.tools.order_tool import check_order_status_tool
from agent.tools.ticket_tool import create_ticket_tool
from agent.tools.email_tool import send_email_tool


class FakeToolCallingChatModel(FakeMessagesListChatModel):
    """A FakeMessagesListChatModel that satisfies create_tool_calling_agent's
    `hasattr(llm, "bind_tools")` requirement by ignoring the tool schemas and
    just returning itself -- the canned `responses` already encode which tool
    calls to emit."""

    def bind_tools(self, tools, **kwargs):
        return self


def _build_agent_with_responses(responses):
    fake_llm = FakeToolCallingChatModel(responses=responses)
    with patch("agent.agent.ChatGoogleGenerativeAI", return_value=fake_llm):
        return SmartOpsAgent()


class TestToolRegistration:

    def test_all_expected_tools_are_wired(self):
        agent = _build_agent_with_responses([AIMessage(content="noop")])
        tool_names = {tool.name for tool in agent.tools}
        assert tool_names == {
            "search_company_policy_and_db",
            "check_order_status",
            "list_user_orders_tool",
            "cancel_order_tool",
            "update_delivery_address_tool",
            "request_order_return_tool",
            "create_order_tool",
            "search_products_tool",
            "get_product_details_tool",
            "get_user_summary_tool",
            "create_ticket",
            "list_user_tickets_tool",
            "update_ticket_status_tool",
            "send_email_notification",
            "check_transaction_status",
        }


class TestOrderStatusScenario:

    def test_order_lookup_invokes_order_tool_and_returns_final_answer(self):
        responses = [
            AIMessage(
                content="",
                tool_calls=[
                    {"name": "check_order_status", "args": {"order_id": "VN1024"}, "id": "call_1"}
                ],
            ),
            AIMessage(content="Your order VN1024 is currently In Transit."),
        ]
        agent = _build_agent_with_responses(responses)

        with patch.object(
            check_order_status_tool,
            "_run",
            return_value="Order ID: VN1024\nStatus: In Transit",
        ) as mock_run:
            result = agent.invoke("What's the status of my order VN1024?")

        mock_run.assert_called_once_with(order_id="VN1024")
        assert result == "Your order VN1024 is currently In Transit."


class TestTicketAndEmailScenario:

    def test_reported_issue_chains_order_lookup_ticket_and_email(self):
        """Mirrors the SYSTEM_PROMPT's documented flow: look up the order for its
        user_id, create a ticket, then send a confirmation email."""
        responses = [
            AIMessage(
                content="",
                tool_calls=[
                    {"name": "check_order_status", "args": {"order_id": "VN1024"}, "id": "call_1"}
                ],
            ),
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "create_ticket",
                        "args": {"user_id": "U00421", "issue": "Item arrived damaged"},
                        "id": "call_2",
                    }
                ],
            ),
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "send_email_notification",
                        "args": {
                            "payload": "user_id=U00421; subject=Ticket created; content=We are on it."
                        },
                        "id": "call_3",
                    }
                ],
            ),
            AIMessage(content="I've created ticket TKT-7788 and emailed you a confirmation."),
        ]
        agent = _build_agent_with_responses(responses)

        with (
            patch.object(
                check_order_status_tool,
                "_run",
                return_value="Order ID: VN1024\nUser ID: U00421\nStatus: In Transit",
            ) as mock_order_run,
            patch.object(
                create_ticket_tool, "_run", return_value="Support ticket TKT-7788 has been created."
            ) as mock_ticket_run,
            patch.object(
                send_email_tool, "_run", return_value="Email sent to Nguyen Van An."
            ) as mock_email_run,
        ):
            result = agent.invoke("My order VN1024 arrived damaged, please help.")

        mock_order_run.assert_called_once_with(order_id="VN1024")
        mock_ticket_run.assert_called_once_with(user_id="U00421", issue="Item arrived damaged")
        mock_email_run.assert_called_once_with(
            payload="user_id=U00421; subject=Ticket created; content=We are on it."
        )
        assert result == "I've created ticket TKT-7788 and emailed you a confirmation."
