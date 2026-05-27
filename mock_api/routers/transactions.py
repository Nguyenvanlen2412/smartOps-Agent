# mock_api/routers/transactions.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from mock_api.mock_db import TRANSACTIONS

class TransactionResponse(BaseModel):
    transaction_id: str
    user_id: str
    amount_vnd: float
    payment_method: str  # "VNPay QR", "MoMo", "Cash on Delivery", etc.
    status: str  # "Success", "Pending", "Failed", "Refunded", etc.
    timestamp: str
    linked_order: Optional[str] = None
    note: Optional[str] = None

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.get("/{txn_id}", response_model=TransactionResponse, summary="Get transaction details")
def get_transaction(txn_id: str):
    """
    Retrieve payment transaction details by ID.
    
    Shows payment status, amount, method (VNPay QR, MoMo, etc.), and linked order.
    This endpoint demonstrates understanding of payment transaction lifecycles.
    
    Returns:
        - transaction_id: Transaction identifier
        - status: "Success", "Pending", "Failed", "Refunded", etc.
        - amount_vnd: Payment amount in Vietnamese Dong
        - payment_method: Payment method used (VNPay QR, MoMo, Internet Banking, etc.)
        - linked_order: Associated order ID (if any)
        - timestamp: When the transaction was created
    
    Raises:
        HTTPException 404: If transaction not found
    
    Example:
        GET /transactions/TXN-20250520-01133
        Returns a "Pending" status to test agent handling of incomplete payments.
    """
    if txn_id not in TRANSACTIONS:
        print(f"[TRANSACTION LOOKUP FAILED] ID: {txn_id} - Not found")
        raise HTTPException(status_code=404, detail=f"Transaction {txn_id} not found")
    
    txn = TRANSACTIONS[txn_id]
    print(f"[TRANSACTION RETRIEVED] ID: {txn_id} | Status: {txn['status']} | Amount: {txn['amount_vnd']} VND | Method: {txn['payment_method']}")
    
    return txn
