import httpx
import os
from langchain_core.tools import StructuredTool


def check_transaction_status(transaction_id: str) -> str:
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        r = httpx.get(f"{base_url}/transactions/{transaction_id}", timeout=5)
        if r.status_code != 200:
            return (
                f"Sorry, I couldn't find any information for Transaction ID "
                f"'{transaction_id}'. Please double-check the ID and try again."
            )
        transaction = r.json()
        return (
            f"Transaction ID: {transaction['transaction_id']}\n"
            f"User ID: {transaction['user_id']}\n"
            f"Status: {transaction['status']}\n"
            f"Payment Method: {transaction['payment_method']}\n"
            f"Transaction Date: {transaction['timestamp']}\n"
            f"Amount (VND): {transaction['amount_vnd']}\n"
            f"Linked Order: {transaction.get('linked_order') or 'N/A'}"
        )
    except Exception as e:
        return f"Error checking transaction: {str(e)}"
    

check_transaction_status_tool = StructuredTool.from_function(
    name="check_transaction_status",
    description="Use this tool to check the status of a transaction. The input should be the transaction ID (e.g., 'TXN12345').",
    func=check_transaction_status
)