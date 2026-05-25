# mock_api/routers/orders.py
from fastapi import APIRouter, HTTPException, status
from mock_api.mock_db import TICKETS

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.get("/{ticket_id}", summary="Get ticket details by ID")
def get_ticket(ticket_id: str):
    """
    Look up a ticket's status, priority, and other details.
    This is the endpoint utilized by the AI agent's ticketing tools.
    """
    # Normalize input string if necessary (e.g., stripping whitespace or uppercase)
    clean_id = ticket_id.strip().upper()
    
    ticket = TICKETS.get(clean_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket ID '{ticket_id}' not found in our system. Please double-check the ID and try again."
        )
    return ticket