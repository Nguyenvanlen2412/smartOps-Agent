# mock_api/routers/tickets.py
from fastapi import APIRouter
from pydantic import BaseModel
import random
from datetime import datetime
from mock_api.mock_db import TICKETS

class TicketRequest(BaseModel):
    user_id: str
    issue: str

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.post("", summary="Create a support ticket")
def create_ticket(body: TicketRequest):
    ticket_id = f"TKT-{random.randint(1000, 9999)}"
    
    ticket = {
        "ticket_id": ticket_id,
        "user_id": body.user_id,
        "issue": body.issue,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }
    
    TICKETS[ticket_id] = ticket    
    # Log to stdout for demo visibility
    print(f"[TICKET CREATED] ID: {ticket_id} | User: {body.user_id} | Issue: {body.issue}")
    
    return {
        "ticket_id": ticket_id,
        "status": "created",
        "user_id": body.user_id
    }
