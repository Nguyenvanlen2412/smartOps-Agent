import httpx
import os
from typing import Optional
from langchain_core.tools import tool


@tool("create_ticket")
def create_ticket_tool(user_id: str, issue: str) -> str:
    """Use this tool to create a support ticket. Create a support ticket using the customer user_id and issue description."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        r = httpx.post(
            f"{base_url}/tickets",
            json={"user_id": user_id, "issue": issue},
            timeout=5,
        )
        if r.status_code != 200:
            return (
                f"Failed to create ticket. Status: {r.status_code} "
                f"Response: {r.text}"
            )
        data = r.json()
        ticket_id = data.get("ticket_id")
        if not ticket_id:
            return "Error: No ticket ID in response"
        return f"Support ticket {ticket_id} has been created for user {user_id}."
    except Exception as e:
        return f"Error creating ticket: {str(e)}"


@tool
def list_user_tickets_tool(user_id: str) -> str:
    """Use this tool to list all support tickets submitted by a customer using their user_id (e.g., 'U00421')."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        r = httpx.get(f"{base_url}/tickets/user/{user_id}", timeout=5)
        if r.status_code != 200:
            return f"Could not find support tickets for User ID '{user_id}'."
        tickets = r.json()
        if not tickets:
            return f"No support tickets found for User ID '{user_id}'."

        lines = [f"Found {len(tickets)} support ticket(s) for User ID {user_id}:"]
        for t in tickets:
            lines.append(
                f"- Ticket ID: {t['ticket_id']} | Status: {t['status']} | Priority: {t.get('priority') or 'Normal'} | "
                f"Issue: {t['issue']} | Resolution: {t.get('resolution') or 'Pending'}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error listing tickets: {str(e)}"


@tool
def update_ticket_status_tool(ticket_id: str, status: Optional[str] = None, priority: Optional[str] = None, resolution: Optional[str] = None) -> str:
    """Use this tool to update or escalate a support ticket's status, priority level, or resolution notes."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        payload = {}
        if status:
            payload["status"] = status
        if priority:
            payload["priority"] = priority
        if resolution:
            payload["resolution"] = resolution

        r = httpx.patch(f"{base_url}/tickets/{ticket_id}", json=payload, timeout=5)
        if r.status_code != 200:
            return f"Failed to update Ticket '{ticket_id}': {r.text}"
        data = r.json()
        return (
            f"Support ticket '{ticket_id}' updated successfully. "
            f"Status: {data['status']} | Priority: {data.get('priority') or 'Normal'} | "
            f"Assigned To: {data.get('assigned_to') or 'Unassigned'}."
        )
    except Exception as e:
        return f"Error updating ticket: {str(e)}"