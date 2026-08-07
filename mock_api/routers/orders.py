# mock_api/routers/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Optional, List
import random
from datetime import datetime, timedelta
from mock_api.database import get_db
from mock_api.models import OrderTable, OrderItemTable


class CreateOrderItem(BaseModel):
    name: str
    quantity: int
    price_vnd: int


class CreateOrderRequest(BaseModel):
    user_id: str
    customer: str
    items: List[CreateOrderItem]
    payment: str
    delivery_address: Optional[str] = None
    note: Optional[str] = None


class CancelOrderRequest(BaseModel):
    reason: Optional[str] = "Customer requested cancellation"


class UpdateAddressRequest(BaseModel):
    new_address: str


class ReturnOrderRequest(BaseModel):
    reason: str
    refund_method: Optional[str] = "Original payment method"


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


def format_order(order: OrderTable) -> dict:
    """Format OrderTable instance with explicit dict representation and items."""
    return {
        "order_id": order.order_id,
        "customer": order.customer,
        "user_id": order.user_id,
        "status": order.status,
        "payment": order.payment,
        "order_date": order.order_date,
        "estimated_delivery": order.estimated_delivery,
        "delivered_date": order.delivered_date,
        "carrier": order.carrier,
        "tracking_number": order.tracking_number,
        "delivery_address": order.delivery_address,
        "note": order.note,
        "return_reason": order.return_reason,
        "return_status": order.return_status,
        "refund_method": order.refund_method,
        "estimated_refund_date": order.estimated_refund_date,
        "cancellation_reason": order.cancellation_reason,
        "refund_status": order.refund_status,
        "items": [
            {"name": item.name, "quantity": item.quantity, "price_vnd": item.price_vnd}
            for item in order.items
        ]
    }


@router.post("", summary="Create a new customer order (Checkout)")
def create_order(body: CreateOrderRequest, db: Session = Depends(get_db)):
    # Generate unique ID with fallback check
    while True:
        order_id = f"VN{random.randint(1000, 9999)}"
        if not db.exec(select(OrderTable).where(OrderTable.order_id == order_id)).first():
            break

    today_str = datetime.now().strftime("%Y-%m-%d")
    eta_str = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    new_order = OrderTable(
        order_id=order_id,
        customer=body.customer,
        user_id=body.user_id.strip().upper(),  # Normalized ID
        status="Processing",
        payment=body.payment,
        order_date=today_str,
        estimated_delivery=eta_str,
        carrier="Giao Hang Nhanh (GHN)",
        tracking_number=f"GHN-{random.randint(10000000, 99999999)}",
        delivery_address=body.delivery_address,
        note=body.note
    )
    db.add(new_order)

    for item in body.items:
        db_item = OrderItemTable(
            order_id=order_id,
            name=item.name,
            quantity=item.quantity,
            price_vnd=item.price_vnd
        )
        db.add(db_item)
        
    db.commit()  # Single atomic transaction
    db.refresh(new_order)

    return format_order(new_order)


@router.get("/user/{user_id}", summary="Get all orders for a customer")
def list_user_orders(user_id: str, db: Session = Depends(get_db)):
    clean_id = user_id.strip().upper()
    orders = db.exec(select(OrderTable).where(OrderTable.user_id == clean_id)).all()
    return [format_order(o) for o in orders]


@router.get("/{order_id}", summary="Get order details by ID")
def get_order(order_id: str, db: Session = Depends(get_db)):
    clean_id = order_id.strip().upper()
    order = db.exec(select(OrderTable).where(OrderTable.order_id == clean_id)).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order ID '{order_id}' not found in our system."
        )

    return format_order(order)


@router.post("/{order_id}/cancel", summary="Cancel an existing order")
def cancel_order(order_id: str, body: CancelOrderRequest, db: Session = Depends(get_db)):
    clean_id = order_id.strip().upper()
    order = db.exec(select(OrderTable).where(OrderTable.order_id == clean_id)).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order '{order_id}' not found.")

    if order.status not in ["Pending Payment", "Processing"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order '{order_id}' cannot be cancelled as its current status is '{order.status}'."
        )

    order.status = "Cancelled"
    order.cancellation_reason = body.reason
    order.refund_status = "Refund process initiated"
    db.add(order)
    db.commit()
    db.refresh(order)

    return format_order(order)


@router.patch("/{order_id}/address", summary="Update delivery address for an order")
def update_delivery_address(order_id: str, body: UpdateAddressRequest, db: Session = Depends(get_db)):
    clean_id = order_id.strip().upper()
    order = db.exec(select(OrderTable).where(OrderTable.order_id == clean_id)).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order '{order_id}' not found.")

    if order.status in ["Delivered", "Cancelled", "Return Requested"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update delivery address for order with status '{order.status}'."
        )

    order.delivery_address = body.new_address
    db.add(order)
    db.commit()
    db.refresh(order)

    return format_order(order)


@router.post("/{order_id}/return", summary="Submit a return / refund request")
def request_order_return(order_id: str, body: ReturnOrderRequest, db: Session = Depends(get_db)):
    clean_id = order_id.strip().upper()
    order = db.exec(select(OrderTable).where(OrderTable.order_id == clean_id)).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order '{order_id}' not found.")

    if order.status not in ["Delivered", "Shipped", "In Transit"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot initiate return for order with status '{order.status}'."
        )

    order.status = "Return Requested"
    order.return_reason = body.reason
    order.return_status = "Approved – Awaiting pickup"
    order.refund_method = body.refund_method
    order.estimated_refund_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

    db.add(order)
    db.commit()
    db.refresh(order)

    return format_order(order)