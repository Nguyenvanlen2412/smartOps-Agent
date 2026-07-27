# mock_api/routers/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from mock_api.database import get_db
from mock_api.models import OrderTable

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get("/{order_id}", summary="Get order details by ID")
def get_order(order_id: str, db: Session = Depends(get_db)):
    """
    Look up an order status, carrier, tracking number, and estimated delivery.
    This is the endpoint utilized by the AI agent's tracking tools.
    """
    clean_id = order_id.strip().upper()

    statement = select(OrderTable).where(OrderTable.order_id == clean_id)
    order = db.exec(statement).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order ID '{order_id}' not found in our system. Please double-check the ID and try again."
        )

    # Convert to dict and format items list for API consumption
    order_dict = order.model_dump()
    order_dict["items"] = [item.model_dump() for item in order.items]
    return order_dict