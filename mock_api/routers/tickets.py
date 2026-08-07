# mock_api/routers/tickets.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Optional
import random
from datetime import datetime
from mock_api.database import get_db
from mock_api.models import TicketTable


class TicketRequest(BaseModel):
    user_id: str
    issue: str


class TicketUpdateRequest(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None
    priority: Optional[str] = None


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


@router.get("/user/{user_id}", summary="Get all support tickets for a user")
def list_user_tickets(user_id: str, db: Session = Depends(get_db)):
    clean_id = user_id.strip().upper()
    tickets = db.exec(select(TicketTable).where(TicketTable.user_id == clean_id)).all()
    return [t.model_dump() for t in tickets]


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


@router.patch("/{ticket_id}", summary="Update ticket status, assignment, or resolution")
def update_ticket(ticket_id: str, body: TicketUpdateRequest, db: Session = Depends(get_db)):
    clean_id = ticket_id.strip().upper()
    statement = select(TicketTable).where(TicketTable.ticket_id == clean_id)
    ticket = db.exec(statement).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket ID '{ticket_id}' not found."
        )

    if body.status:
        ticket.status = body.status
    if body.assigned_to:
        ticket.assigned_to = body.assigned_to
    if body.resolution:
        ticket.resolution = body.resolution
    if body.priority:
        ticket.priority = body.priority

    ticket.last_update = datetime.now().isoformat()
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket.model_dump()
