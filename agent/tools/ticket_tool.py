import httpx
import os
from langchain_core.tools import StructuredTool

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def create_ticket(user_id: str, issue: str) -> str:
    """
    Create a support ticket for a user.
    
    Args:
        user_id: The customer ID (e.g., "U00421")
        issue: Description of the problem
    
    Returns:
        Success message with ticket ID or error message
    """
    try:
        r = httpx.post(
            f"{API_BASE_URL}/tickets",
            json={"user_id": user_id, "issue": issue},
            timeout=5
        )
        
        if r.status_code != 200:
            return (f"Failed to create ticket. Status: {r.status_code}"
                    f" Response: {r.text}")
        
        data = r.json()
        ticket_id = data.get("ticket_id")
        
        if not ticket_id:
            return "Error: No ticket ID in response"
        
        return f"Support ticket {ticket_id} has been created for user {user_id}."
    
    except Exception as e:
        return f"Error creating ticket: {str(e)}"
    
create_ticket_tool = StructuredTool.from_function(
    name="create_ticket",
    description="Use this tool to create a support ticket. Create a support ticket using the customer user_id and issue description.",
    func=create_ticket
    )