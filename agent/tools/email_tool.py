import httpx
import os
import re
from langchain_core.tools import BaseTool
from pydantic import Field


class EmailTool(BaseTool):
    """Send a confirmation email to a customer after an action like creating a ticket."""

    name: str = "send_email_notification"
    description: str = (
        "Use this to send a confirmation email to a customer after completing "
        "an action like creating a ticket or resolving an order issue. "
        "Input must be formatted exactly as: "
        "user_id=U00XXX; subject=...; content=..."
    )
    base_url: str = Field(
        default_factory=lambda: os.getenv("MOCK_API_BASE_URL", "http://localhost:8000")
    )

    def _parse_payload(self, payload: str) -> dict:
        """Extract user_id, subject, and content from the semicolon-delimited payload."""
        user_id_match = re.search(r'user_id\s*=\s*(U\d+)', payload)
        subject_match = re.search(r'subject\s*=\s*(.+?)(?:\s*;\s*content\s*=|$)', payload)
        content_match = re.search(r'content\s*=\s*(.+)', payload)

        errors = []
        if not user_id_match:
            errors.append("could not parse user_id")
        if not subject_match:
            errors.append("could not parse subject")
        if not content_match:
            errors.append("could not parse content")
        if errors:
            raise ValueError(
                f"Email tool error: {'; '.join(errors)}. "
                "Expected format: user_id=U00XXX; subject=...; content=..."
            )

        return {
            "user_id": user_id_match.group(1).strip(),
            "subject": subject_match.group(1).strip(),
            "message": content_match.group(1).strip(),
        }

    def _run(self, payload: str) -> str:
        try:
            data = self._parse_payload(payload)
            r = httpx.post(f"{self.base_url}/emails/notify", json=data)
            if r.status_code == 404:
                return "Could not send email: user not found."
            resp = r.json()
            return (
                f"Email sent to {resp['recipient_name']} "
                f"({resp['recipient_email']}) — subject: \"{resp['subject']}\"."
            )
        except ValueError as ve:
            return str(ve)
        except Exception as e:
            return f"Email tool error: {str(e)}"


# Instantiate for use by the agent
send_email_tool = EmailTool()