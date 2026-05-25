# mock_api/routers/orders.py
from fastapi import APIRouter, HTTPException, status
from mock_api.mock_db import TRANSACTIONS

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.get("/{transaction_id}", summary="Get transaction details by ID")
def get_transaction(transaction_id: str):
    """
    Look up a transaction's status, amount, and other details.
    This is the endpoint utilized by the AI agent's transaction tools.
    """
    # Normalize input string if necessary (e.g., stripping whitespace or uppercase)
    clean_id = transaction_id.strip().upper()
    
    transaction = TRANSACTIONS.get(clean_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction ID '{transaction_id}' not found in our system. Please double-check the ID and try again."
        )
    return transaction