# mock_api/routers/transactions.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Session, select
from mock_api.database import get_db
from mock_api.models import TransactionTable


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
def get_transaction(txn_id: str, db: Session = Depends(get_db)):
    """
    Retrieve payment transaction details by ID.
    Shows payment status, amount, method, and linked order.
    """
    clean_id = txn_id.strip()
    statement = select(TransactionTable).where(TransactionTable.transaction_id == clean_id)
    txn = db.exec(statement).first()

    if not txn:
        print(f"[TRANSACTION LOOKUP FAILED] ID: {clean_id} - Not found")
        raise HTTPException(status_code=404, detail=f"Transaction '{clean_id}' not found")

    print(f"[TRANSACTION RETRIEVED DB] ID: {clean_id} | Status: {txn.status} | Amount: {txn.amount_vnd} VND | Method: {txn.payment_method}")
    return txn.model_dump()
