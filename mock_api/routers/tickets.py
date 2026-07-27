# mock_api/routers/tickets.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
import random
from datetime import datetime
from mock_api.database import get_db
from mock_api.models import TicketTable


class TicketRequest(BaseModel):
    user_id: str
    issue: str


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post("", summary="Create a support ticket")
def create_ticket(body: TicketRequest, db: Session = Depends(get_db)):
    ticket_id = f"TKT-{random.randint(1000, 9999)}"
    now_iso = datetime.now().isoformat()

    ticket_record = TicketTable(
        ticket_id=ticket_id,
        user_id=body.user_id,
        issue=body.issue,
        status="open",
        created=now_iso,
        created_at=now_iso,
        last_update=now_iso
    )

    db.add(ticket_record)
    db.commit()
    db.refresh(ticket_record)

    print(f"[TICKET CREATED DB] ID: {ticket_id} | User: {body.user_id} | Issue: {body.issue}")

    return {
        "ticket_id": ticket_id,
        "status": "created",
        "user_id": body.user_id
    }


@router.get("/{ticket_id}", summary="Get ticket status and details")
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    clean_id = ticket_id.strip().upper()
    statement = select(TicketTable).where(TicketTable.ticket_id == clean_id)
    ticket = db.exec(statement).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket ID '{ticket_id}' not found."
        )
    return ticket.model_dump()
