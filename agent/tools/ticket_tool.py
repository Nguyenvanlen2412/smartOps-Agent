import httpx
import os
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class TicketInput(BaseModel):
    """Input schema for the ticket creation tool."""
    user_id: str = Field(description="The customer ID (e.g., 'U00421')")
    issue: str = Field(description="Description of the problem")


class TicketTool(BaseTool):
    """Create a support ticket for a user."""

    name: str = "create_ticket"
    description: str = (
        "Use this tool to create a support ticket. "
        "Create a support ticket using the customer user_id and issue description."
    )
    args_schema: type[BaseModel] = TicketInput
    base_url: str = Field(
        default_factory=lambda: os.getenv("API_BASE_URL", "http://localhost:8000")
    )

    def _run(self, user_id: str, issue: str) -> str:
        try:
            r = httpx.post(
                f"{self.base_url}/tickets",
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


# Instantiate for use by the agent
create_ticket_tool = TicketTool()