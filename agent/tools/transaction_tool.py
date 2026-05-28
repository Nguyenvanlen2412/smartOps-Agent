import httpx
import os
from langchain_core.tools import StructuredTool

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def check_transaction_status(transaction_id: str) -> str:
    r = httpx.get(f"{API_BASE_URL}/transactions/{transaction_id}")
    if r.status_code == 200:
        transaction = r.json()
        return (
            f"Transaction ID: {transaction_id}\n"
            f"Customer: {transaction['customer']}\n"
            f"User ID: {transaction['user_id']}\n"
            f"Status: {transaction['status']}\n"
            f"Transaction Date: {transaction['transaction_date']}\n"
            f"Amount: {transaction['amount']}"
        )
    else: 
        return f"Sorry, I couldn't find any information for Transaction ID '{transaction_id}'. Please double-check the ID and try again."
    

check_transaction_status_tool = StructuredTool.from_function(
    name="check_transaction_status",
    description="Use this tool to check the status of a transaction. The input should be the transaction ID (e.g., 'TXN12345').",
    func=check_transaction_status
)