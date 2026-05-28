import httpx
import os
from langchain_core.tools import BaseTool
from pydantic import Field


class OrderTool(BaseTool):
    """Check the status of a customer order by order ID."""

    name: str = "check_order_status"
    description: str = (
        "Use this tool to check the status of an order. "
        "The input should be the order ID (e.g., 'VN12345')."
    )
    base_url: str = Field(
        default_factory=lambda: os.getenv("API_BASE_URL", "http://localhost:8000")
    )

    def _run(self, order_id: str) -> str:
        try:
            r = httpx.get(f"{self.base_url}/orders/{order_id}", timeout=5)
            if r.status_code != 200:
                return (
                    f"Sorry, I couldn't find any information for Order ID '{order_id}'. "
                    "Please double-check the ID and try again."
                )
            order = r.json()
            return (
                f"Order ID: {order_id}\n"
                f"Customer: {order['customer']}\n"
                f"User ID: {order['user_id']}\n"
                f"Status: {order['status']}\n"
                f"Order Date: {order['order_date']}\n"
                f"Payment: {order['payment']}"
            )
        except Exception as e:
            return f"Error checking order: {str(e)}"


# Instantiate for use by the agent
check_order_status_tool = OrderTool()