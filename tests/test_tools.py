from unittest.mock import MagicMock, patch

from agent.tools.rag_tool import rag_tool
from agent.tools.order_tool import (
    check_order_status_tool,
    list_user_orders_tool,
    cancel_order_tool,
    update_delivery_address_tool,
    request_order_return_tool,
    create_order_tool,
)
from agent.tools.ticket_tool import (
    create_ticket_tool,
    list_user_tickets_tool,
    update_ticket_status_tool,
)
from agent.tools.email_tool import send_email_tool
from agent.tools.transaction_tool import check_transaction_status, check_transaction_status_tool
from agent.tools.product_tool import search_products_tool, get_product_details_tool
from agent.tools.user_tool import get_user_summary_tool


class TestRAGTool:

    @patch("agent.tools.rag_tool._get_qa_chain")
    def test_run_success_with_context(self, mock_get_chain):
        """Successful run formats the answer plus numbered source documents."""
        mock_chain = MagicMock()
        doc_1 = MagicMock(page_content="Refunds are processed within 5-7 business days.")
        doc_2 = MagicMock(page_content="Items must be returned in original packaging.")
        mock_chain.invoke.return_value = {
            "answer": "You can get a refund within 5-7 days.",
            "context": [doc_1, doc_2],
        }
        mock_get_chain.return_value = mock_chain
        query = "What is the refund policy?"

        result = rag_tool.invoke({"query": query})

        mock_chain.invoke.assert_called_once_with({"input": query})
        assert "Answer:\nYou can get a refund within 5-7 days." in result
        assert "Source 1:\nRefunds are processed within 5-7 business days." in result
        assert "Source 2:\nItems must be returned in original packaging." in result

    @patch("agent.tools.rag_tool._get_qa_chain")
    def test_run_no_context(self, mock_get_chain):
        """Run with no retrieved documents still returns the answer with an empty source section."""
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {
            "answer": "No specific policy found.",
            "context": [],
        }
        mock_get_chain.return_value = mock_chain

        result = rag_tool.invoke({"query": "Some obscure question"})

        assert "Answer:\nNo specific policy found." in result
        assert result.endswith("Source Documents:\n")

    @patch("agent.tools.rag_tool._get_qa_chain")
    def test_run_missing_answer_key(self, mock_get_chain):
        """Falls back to a default message when the chain response has no 'answer' key."""
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {"context": []}
        mock_get_chain.return_value = mock_chain

        result = rag_tool.invoke({"query": "Test query"})

        assert "Answer:\nNo answer found." in result

    @patch("agent.tools.rag_tool._get_qa_chain")
    def test_run_exception_handling(self, mock_get_chain):
        """Exceptions raised by the chain are caught and returned as an error string, not raised."""
        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = Exception("LLM connection timeout")
        mock_get_chain.return_value = mock_chain

        result = rag_tool.invoke({"query": "Test query"})

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
                "items": [{"name": "Samsung Galaxy A55 5G", "quantity": 1}],
            },
        )

        result = check_order_status_tool.invoke({"order_id": "VN1024"})

        mock_get.assert_called_once()
        assert mock_get.call_args.args[0].endswith("/orders/VN1024")
        assert "Customer: Nguyen Van An" in result
        assert "Status: In Transit" in result

    @patch("agent.tools.order_tool.httpx.get")
    def test_run_not_found(self, mock_get):
        mock_get.return_value = MagicMock(status_code=404)

        result = check_order_status_tool.invoke({"order_id": "VN9999"})

        assert "couldn't find any information for Order ID 'VN9999'" in result

    @patch("agent.tools.order_tool.httpx.get")
    def test_run_exception_handling(self, mock_get):
        mock_get.side_effect = Exception("connection refused")

        result = check_order_status_tool.invoke({"order_id": "VN1024"})

        assert result == "Error checking order: connection refused"

    def test_tool_configuration(self):
        assert check_order_status_tool.name == "check_order_status"


class TestExpandedEcomTools:

    @patch("agent.tools.product_tool.httpx.get")
    def test_search_products_tool(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: [
                {"product_id": "PROD-001", "name": "Samsung Galaxy A55 5G", "category": "Mobile Phones", "price_vnd": 9490000, "stock_quantity": 15, "warranty_months": 12}
            ]
        )
        result = search_products_tool.invoke({"query": "Samsung"})
        assert "Samsung Galaxy A55 5G" in result

    @patch("agent.tools.product_tool.httpx.get")
    def test_get_product_details_tool(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "product_id": "PROD-001", "name": "Samsung Galaxy A55 5G", "category": "Mobile Phones",
                "price_vnd": 9490000, "stock_quantity": 15, "warranty_months": 12, "description": "Super AMOLED"
            }
        )
        result = get_product_details_tool.invoke({"product_id": "PROD-001"})
        assert "Product ID: PROD-001" in result
        assert "Stock Available: 15 units" in result

    @patch("agent.tools.user_tool.httpx.get")
    def test_get_user_summary_tool(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "user_id": "U00421", "name": "Nguyen Van An", "email": "van.an@gmail.com",
                "total_orders": 2, "active_orders_count": 1, "active_orders": ["VN1024"],
                "total_tickets": 1, "open_tickets_count": 0, "open_tickets": []
            }
        )
        result = get_user_summary_tool.invoke({"user_id": "U00421"})
        assert "User Profile for Nguyen Van An" in result
        assert "Active Orders (1): VN1024" in result

    @patch("agent.tools.order_tool.httpx.post")
    def test_cancel_order_tool(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"order_id": "VN1029", "status": "Cancelled", "refund_status": "Initiated"}
        )
        result = cancel_order_tool.invoke({"order_id": "VN1029", "reason": "Test"})
        assert "successfully CANCELLED" in result

    @patch("agent.tools.ticket_tool.httpx.get")
    def test_list_user_tickets_tool(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: [
                {"ticket_id": "TKT-0881", "status": "In Progress", "priority": "High", "issue": "Defective", "resolution": None}
            ]
        )
        result = list_user_tickets_tool.invoke({"user_id": "U00654"})
        assert "TKT-0881" in result

    @patch("agent.tools.ticket_tool.httpx.post")
    def test_create_ticket_tool(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"ticket_id": "TKT-0999"}
        )
        result = create_ticket_tool.invoke({"user_id": "U00421", "issue": "Screen flickering"})
        assert "Support ticket TKT-0999 has been created for user U00421." in result

    @patch("agent.tools.ticket_tool.httpx.patch")
    def test_update_ticket_status_tool(self, mock_patch):
        mock_patch.return_value = MagicMock(
            status_code=200,
            json=lambda: {"status": "Resolved", "priority": "High", "assigned_to": "Tech Team"}
        )
        result = update_ticket_status_tool.invoke({"ticket_id": "TKT-0999", "status": "Resolved"})
        assert "Support ticket 'TKT-0999' updated successfully." in result
