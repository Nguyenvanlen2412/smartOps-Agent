from unittest.mock import MagicMock, patch

from agent.tools.rag_tool import RAGTool, rag_tool
from agent.tools.order_tool import OrderTool, check_order_status_tool
from agent.tools.ticket_tool import TicketTool, create_ticket_tool
from agent.tools.email_tool import EmailTool, send_email_tool
from agent.tools.transaction_tool import check_transaction_status, check_transaction_status_tool


def _tool_with_mock_chain(mock_chain):
    """Build a fresh RAGTool with its lazily-created qa_chain pre-populated."""
    tool = RAGTool()
    tool._qa_chain = mock_chain
    return tool


class TestRAGTool:

    def test_run_success_with_context(self):
        """Successful run formats the answer plus numbered source documents."""
        mock_chain = MagicMock()
        doc_1 = MagicMock(page_content="Refunds are processed within 5-7 business days.")
        doc_2 = MagicMock(page_content="Items must be returned in original packaging.")
        mock_chain.invoke.return_value = {
            "answer": "You can get a refund within 5-7 days.",
            "context": [doc_1, doc_2],
        }
        tool = _tool_with_mock_chain(mock_chain)
        query = "What is the refund policy?"

        result = tool._run(query)

        mock_chain.invoke.assert_called_once_with({"input": query})
        assert "Answer:\nYou can get a refund within 5-7 days." in result
        assert "Source 1:\nRefunds are processed within 5-7 business days." in result
        assert "Source 2:\nItems must be returned in original packaging." in result

    def test_run_no_context(self):
        """Run with no retrieved documents still returns the answer with an empty source section."""
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {
            "answer": "No specific policy found.",
            "context": [],
        }
        tool = _tool_with_mock_chain(mock_chain)

        result = tool._run("Some obscure question")

        assert "Answer:\nNo specific policy found." in result
        assert result.endswith("Source Documents:\n")

    def test_run_missing_answer_key(self):
        """Falls back to a default message when the chain response has no 'answer' key."""
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {"context": []}
        tool = _tool_with_mock_chain(mock_chain)

        result = tool._run("Test query")

        assert "Answer:\nNo answer found." in result

    def test_run_exception_handling(self):
        """Exceptions raised by the chain are caught and returned as an error string, not raised."""
        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = Exception("LLM connection timeout")
        tool = _tool_with_mock_chain(mock_chain)

        result = tool._run("Test query")

        assert result == "An error occurred while processing your request: LLM connection timeout"

    def test_tool_configuration(self):
        """The module-level tool instance is registered with the name/description the agent relies on."""
        assert rag_tool.name == "search_company_policy_and_db"
        assert "Use this tool to search for company policies" in rag_tool.description


class TestOrderTool:

    @patch("agent.tools.order_tool.httpx.get")
    def test_run_success(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "customer": "Nguyen Van An",
                "user_id": "U00421",
                "status": "In Transit",
                "order_date": "2025-05-18",
                "payment": "VNPay QR – Paid",
            },
        )
        tool = OrderTool()

        result = tool._run("VN1024")

        mock_get.assert_called_once()
        assert mock_get.call_args.args[0].endswith("/orders/VN1024")
        assert "Customer: Nguyen Van An" in result
        assert "Status: In Transit" in result

    @patch("agent.tools.order_tool.httpx.get")
    def test_run_not_found(self, mock_get):
        mock_get.return_value = MagicMock(status_code=404)
        tool = OrderTool()

        result = tool._run("VN9999")

        assert "couldn't find any information for Order ID 'VN9999'" in result

    @patch("agent.tools.order_tool.httpx.get")
    def test_run_exception_handling(self, mock_get):
        mock_get.side_effect = Exception("connection refused")
        tool = OrderTool()

        result = tool._run("VN1024")

        assert result == "Error checking order: connection refused"

    def test_tool_configuration(self):
        assert check_order_status_tool.name == "check_order_status"


class TestTicketTool:

    @patch("agent.tools.ticket_tool.httpx.post")
    def test_run_success(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"ticket_id": "TKT-1234", "status": "created", "user_id": "U00421"},
        )
        tool = TicketTool()

        result = tool._run(user_id="U00421", issue="Item arrived damaged")

        mock_post.assert_called_once_with(
            f"{tool.base_url}/tickets",
            json={"user_id": "U00421", "issue": "Item arrived damaged"},
            timeout=5,
        )
        assert result == "Support ticket TKT-1234 has been created for user U00421."

    @patch("agent.tools.ticket_tool.httpx.post")
    def test_run_missing_ticket_id(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {})
        tool = TicketTool()

        result = tool._run(user_id="U00421", issue="Item arrived damaged")

        assert result == "Error: No ticket ID in response"

    @patch("agent.tools.ticket_tool.httpx.post")
    def test_run_failure_status(self, mock_post):
        mock_post.return_value = MagicMock(status_code=500, text="Internal Server Error")
        tool = TicketTool()

        result = tool._run(user_id="U00421", issue="Item arrived damaged")

        assert "Failed to create ticket. Status: 500" in result

    @patch("agent.tools.ticket_tool.httpx.post")
    def test_run_exception_handling(self, mock_post):
        mock_post.side_effect = Exception("connection refused")
        tool = TicketTool()

        result = tool._run(user_id="U00421", issue="Item arrived damaged")

        assert result == "Error creating ticket: connection refused"

    def test_tool_configuration(self):
        assert create_ticket_tool.name == "create_ticket"


class TestEmailTool:

    @patch("agent.tools.email_tool.httpx.post")
    def test_run_success(self, mock_post):
        mock_post.return_value = MagicMock(
            json=lambda: {
                "recipient_name": "Nguyen Van An",
                "recipient_email": "van.an@gmail.com",
                "subject": "Your ticket has been created",
            }
        )
        tool = EmailTool()

        result = tool._run(
            "user_id=U00421; subject=Your ticket has been created; content=We are on it."
        )

        mock_post.assert_called_once_with(
            f"{tool.base_url}/emails/notify",
            json={
                "user_id": "U00421",
                "subject": "Your ticket has been created",
                "message": "We are on it.",
            },
        )
        assert "Email sent to Nguyen Van An (van.an@gmail.com)" in result

    @patch("agent.tools.email_tool.httpx.post")
    def test_run_user_not_found(self, mock_post):
        mock_post.return_value = MagicMock(status_code=404)
        tool = EmailTool()

        result = tool._run("user_id=U99999; subject=Hi; content=Test")

        assert result == "Could not send email: user not found."

    def test_run_malformed_payload(self):
        tool = EmailTool()

        result = tool._run("this payload has no fields")

        assert "could not parse user_id" in result
        assert "could not parse subject" in result
        assert "could not parse content" in result

    @patch("agent.tools.email_tool.httpx.post")
    def test_run_exception_handling(self, mock_post):
        mock_post.side_effect = Exception("connection refused")
        tool = EmailTool()

        result = tool._run("user_id=U00421; subject=Hi; content=Test")

        assert result == "Email tool error: connection refused"

    def test_tool_configuration(self):
        assert send_email_tool.name == "send_email_notification"


class TestTransactionTool:

    @patch("agent.tools.transaction_tool.httpx.get")
    def test_check_transaction_status_success(self, mock_get):
        """Regression test: the tool must read the fields the real API actually returns
        (transaction_id, user_id, status, payment_method, timestamp, amount_vnd,
        linked_order) rather than the nonexistent customer/transaction_date/amount keys."""
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "transaction_id": "TXN-20250518-00421",
                "user_id": "U00421",
                "amount_vnd": 9490000,
                "payment_method": "VNPay QR",
                "status": "Success",
                "timestamp": "2025-05-18 14:32:07",
                "linked_order": "VN1024",
            },
        )

        result = check_transaction_status("TXN-20250518-00421")

        assert "User ID: U00421" in result
        assert "Status: Success" in result
        assert "Amount (VND): 9490000" in result
        assert "Linked Order: VN1024" in result

    @patch("agent.tools.transaction_tool.httpx.get")
    def test_check_transaction_status_not_found(self, mock_get):
        mock_get.return_value = MagicMock(status_code=404)

        result = check_transaction_status("TXN-DOES-NOT-EXIST")

        assert "couldn't find any information for Transaction ID 'TXN-DOES-NOT-EXIST'" in result

    @patch("agent.tools.transaction_tool.httpx.get")
    def test_check_transaction_status_exception_handling(self, mock_get):
        mock_get.side_effect = Exception("connection refused")

        result = check_transaction_status("TXN-20250518-00421")

        assert result == "Error checking transaction: connection refused"

    def test_tool_configuration(self):
        assert check_transaction_status_tool.name == "check_transaction_status"
