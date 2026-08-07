import httpx
import os
from langchain_core.tools import tool


@tool
def get_user_summary_tool(user_id: str) -> str:
    """Use this tool to retrieve a customer's profile, active order IDs, and open ticket IDs using their user_id (e.g., 'U00421')."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        r = httpx.get(f"{base_url}/users/{user_id}/summary", timeout=5)
        if r.status_code != 200:
            return f"User ID '{user_id}' not found."
        data = r.json()
        active_orders = ", ".join(data.get("active_orders", [])) or "None"
        open_tickets = ", ".join(data.get("open_tickets", [])) or "None"
        return (
            f"User Profile for {data['name']} (ID: {data['user_id']}):\n"
            f"- Email: {data['email']}\n"
            f"- Total Orders Placed: {data['total_orders']}\n"
            f"- Active Orders ({data['active_orders_count']}): {active_orders}\n"
            f"- Open Tickets ({data['open_tickets_count']}): {open_tickets}"
        )
    except Exception as e:
        return f"Error fetching user summary: {str(e)}"
