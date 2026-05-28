import httpx
import os
from langchain_core.tools import StructuredTool
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def check_order_status(order_id: str) -> str:
    r = httpx.get(f"{API_BASE_URL}/orders/{order_id}")
    if r.status_code == 200:
        order = r.json()
        return (
            f"Order ID: {order_id}\n"
            f"Customer: {order['customer']}\n"
            f"User ID: {order['user_id']}\n"
            f"Status: {order['status']}\n"
            f"Order Date: {order['order_date']}\n"
            f"Payment: {order['payment']}"
        )
    else: 
        return f"Sorry, I couldn't find any information for Order ID '{order_id}'. Please double-check the ID and try again."
    

check_order_status_tool = StructuredTool.from_function(
    name="check_order_status",
    description="Use this tool to check the status of an order. The input should be the order ID (e.g., 'VN12345').",
    func=check_order_status
)