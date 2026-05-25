# mock_api/routers/orders.py
from fastapi import APIRouter, HTTPException, status
from mock_api.mock_db import ORDERS

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/{order_id}", summary="Get order details by ID")
def get_order(order_id: str):
    """
    Look up an order status, carrier, tracking number, and estimated delivery.
    This is the endpoint utilized by the AI agent's tracking tools.
    """
    # Normalize input string if necessary (e.g., stripping whitespace or uppercase)
    clean_id = order_id.strip().upper()
    
    order = ORDERS.get(clean_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order ID '{order_id}' not found in our system. Please double-check the ID and try again."
        )
    return order