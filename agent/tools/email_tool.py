import httpx
import os
import re
from langchain_core.tools import StructuredTool

BASE = os.getenv("MOCK_API_BASE_URL", "http://localhost:8000")

def send_email_notification(payload: str) -> str:
    """
    payload format (agent must follow this):
    user_id=U00421; subject=Your ticket TKT-0884; content=Dear Nguyen Van An, ...
    """
    try:
        # Robust parsing: use regex to extract key=value pairs
        # Handles variations like missing spaces, extra whitespace, different separators
        user_id_match = re.search(r'user_id\s*=\s*(U\d+)', payload)
        subject_match = re.search(r'subject\s*=\s*(.+?)(?:\s*;\s*content\s*=|$)', payload)
        content_match = re.search(r'content\s*=\s*(.+)', payload)

        if not user_id_match:
            return "Email tool error: could not parse user_id from payload. Expected format: user_id=U00XXX; subject=...; content=..."
        if not subject_match:
            return "Email tool error: could not parse subject from payload."
        if not content_match:
            return "Email tool error: could not parse content from payload."

        user_id = user_id_match.group(1).strip()
        subject = subject_match.group(1).strip()
        content = content_match.group(1).strip()

        r = httpx.post(f"{BASE}/emails/notify", json={
            "user_id": user_id,
            "subject": subject,
            "message": content,
        })
        if r.status_code == 404:
            return "Could not send email: user not found."
        data = r.json()
        return (
            f"Email sent to {data['recipient_name']} "
            f"({data['recipient_email']}) — subject: \"{data['subject']}\"."
        )
    except Exception as e:
        return f"Email tool error: {str(e)}"

send_email_tool = StructuredTool.from_function(
    name="send_email_notification",
    description=(
        "Use this to send a confirmation email to a customer after completing "
        "an action like creating a ticket or resolving an order issue. "
        "Input must be formatted exactly as: "
        "user_id=U00XXX; subject=...; content=..."
    ),
    func=send_email_notification
)