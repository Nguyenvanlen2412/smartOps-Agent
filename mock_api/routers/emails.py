# mock_api/routers/orders.py
from fastapi import APIRouter, HTTPException, status
from mock_api.mock_db import EMAILS

router = APIRouter(
    prefix="/emails",
    tags=["Emails"]
)

@router.get("/{email_id}", summary="Get email details by ID")
def get_email(email_id: str):
    """
    Look up an email status, carrier, tracking number, and estimated delivery.
    This is the endpoint utilized by the AI agent's tracking tools.
    """
    # Normalize input string if necessary (e.g., stripping whitespace or uppercase)
    clean_id = email_id.strip().upper()
    
    email = EMAILS.get(clean_id)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Email ID '{email_id}' not found in our system. Please double-check the ID and try again."
        )
    return email