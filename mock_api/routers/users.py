# mock_api/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from mock_api.database import get_db
from mock_api.models import UserTable, OrderTable, TicketTable

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}", summary="Get user profile by user_id")
def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    clean_id = user_id.strip().upper()
    user = db.exec(select(UserTable).where(UserTable.user_id == clean_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User ID '{user_id}' not found."
        )
    return user.model_dump()


@router.get("/{user_id}/summary", summary="Get customer summary including active orders and tickets")
def get_user_summary(user_id: str, db: Session = Depends(get_db)):
    clean_id = user_id.strip().upper()
    user = db.exec(select(UserTable).where(UserTable.user_id == clean_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User ID '{user_id}' not found."
        )

    orders = db.exec(select(OrderTable).where(OrderTable.user_id == clean_id)).all()
    tickets = db.exec(select(TicketTable).where(TicketTable.user_id == clean_id)).all()

    active_orders = [o for o in orders if o.status in ["Processing", "In Transit", "Shipped", "Pending Payment", "Delayed"]]
    open_tickets = [t for t in tickets if t.status in ["open", "In Progress"]]

    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "total_orders": len(orders),
        "active_orders_count": len(active_orders),
        "active_orders": [o.order_id for o in active_orders],
        "total_tickets": len(tickets),
        "open_tickets_count": len(open_tickets),
        "open_tickets": [t.ticket_id for t in open_tickets]
    }
