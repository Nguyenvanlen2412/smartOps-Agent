import httpx
import os
from typing import Optional, List
from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, Field


@tool("check_order_status")
def check_order_status_tool(order_id: str) -> str:
    """Use this tool to check the status of an order. The input should be the order ID (e.g., 'VN1024')."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        r = httpx.get(f"{base_url}/orders/{order_id}", timeout=5)
        if r.status_code != 200:
            return (
                f"Sorry, I couldn't find any information for Order ID '{order_id}'. "
                "Please double-check the ID and try again."
            )
        order = r.json()
        items_str = ", ".join([f"{item['name']} (x{item['quantity']})" for item in order.get('items', [])])
        return (
            f"Order ID: {order_id}\n"
            f"Customer: {order['customer']}\n"
            f"User ID: {order['user_id']}\n"
            f"Status: {order['status']}\n"
            f"Items: {items_str}\n"
            f"Order Date: {order['order_date']}\n"
            f"Estimated Delivery: {order.get('estimated_delivery') or 'N/A'}\n"
            f"Delivery Address: {order.get('delivery_address') or 'N/A'}\n"
            f"Payment: {order['payment']}"
        )
    except Exception as e:
        return f"Error checking order: {str(e)}"


@tool
def list_user_orders_tool(user_id: str) -> str:
    """Use this tool to list all orders for a customer using their user_id (e.g., 'U00421')."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        r = httpx.get(f"{base_url}/orders/user/{user_id}", timeout=5)
        if r.status_code != 200:
            return f"Could not find orders for User ID '{user_id}'."
        orders = r.json()
        if not orders:
            return f"No orders found for User ID '{user_id}'."

        lines = [f"Found {len(orders)} order(s) for User ID {user_id}:"]
        for o in orders:
            items_summary = ", ".join([f"{i['name']} (x{i['quantity']})" for i in o.get('items', [])])
            lines.append(
                f"- Order ID: {o['order_id']} | Status: {o['status']} | Date: {o['order_date']} | Items: {items_summary}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error listing user orders: {str(e)}"


@tool
def cancel_order_tool(order_id: str, reason: str = "Customer requested cancellation") -> str:
    """Use this tool to cancel an order by order_id (e.g., 'VN1029'). Only orders in 'Pending Payment' or 'Processing' status can be cancelled."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        r = httpx.post(f"{base_url}/orders/{order_id}/cancel", json={"reason": reason}, timeout=5)
        if r.status_code != 200:
            err = r.json().get("detail", r.text)
            return f"Failed to cancel Order '{order_id}': {err}"
        data = r.json()
        return f"Order '{order_id}' has been successfully CANCELLED. Status: {data['status']}. Refund status: {data.get('refund_status')}."
    except Exception as e:
        return f"Error cancelling order: {str(e)}"


@tool
def update_delivery_address_tool(order_id: str, new_address: str) -> str:
    """Use this tool to update the delivery address of an existing order before it ships."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        r = httpx.patch(f"{base_url}/orders/{order_id}/address", json={"new_address": new_address}, timeout=5)
        if r.status_code != 200:
            err = r.json().get("detail", r.text)
            return f"Failed to update address for Order '{order_id}': {err}"
        data = r.json()
        return f"Delivery address for Order '{order_id}' has been updated to: '{data['delivery_address']}'."
    except Exception as e:
        return f"Error updating address: {str(e)}"


@tool
def request_order_return_tool(order_id: str, reason: str, refund_method: str = "Original payment method") -> str:
    """Use this tool to submit a return or refund request for a delivered or shipped order."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        r = httpx.post(
            f"{base_url}/orders/{order_id}/return",
            json={"reason": reason, "refund_method": refund_method},
            timeout=5
        )
        if r.status_code != 200:
            err = r.json().get("detail", r.text)
            return f"Failed to submit return request for Order '{order_id}': {err}"
        data = r.json()
        return (
            f"Return request submitted for Order '{order_id}'. "
            f"Status: {data['return_status']}. "
            f"Reason: {data['return_reason']}. "
            f"Estimated refund date: {data.get('estimated_refund_date')}."
        )
    except Exception as e:
        return f"Error submitting return request: {str(e)}"


@tool
def create_order_tool(user_id: str, customer_name: str, item_name: str, item_price_vnd: int, delivery_address: str, quantity: int = 1, payment: str = "VNPay QR") -> str:
    """Use this tool to place a new customer order (Checkout)."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        payload = {
            "user_id": user_id,
            "customer": customer_name,
            "items": [{"name": item_name, "quantity": quantity, "price_vnd": item_price_vnd}],
            "payment": payment,
            "delivery_address": delivery_address
        }
        r = httpx.post(f"{base_url}/orders", json=payload, timeout=5)
        if r.status_code != 200:
            return f"Failed to create order: {r.text}"
        data = r.json()
        return (
            f"Order successfully created! "
            f"Order ID: {data['order_id']} | Customer: {data['customer']} | "
            f"Status: {data['status']} | Estimated Delivery: {data['estimated_delivery']} | "
            f"Carrier: {data['carrier']} ({data['tracking_number']})."
        )
    except Exception as e:
        return f"Error creating order: {str(e)}"