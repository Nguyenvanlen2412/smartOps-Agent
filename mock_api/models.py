# mock_api/models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class UserTable(SQLModel, table=True):
    __tablename__ = "users"

    user_id: str = Field(primary_key=True)
    name: str
    email: str


class ProductTable(SQLModel, table=True):
    __tablename__ = "products"

    product_id: str = Field(primary_key=True)
    name: str
    category: str
    price_vnd: int
    stock_quantity: int
    description: str
    warranty_months: int = Field(default=12)


class OrderItemTable(SQLModel, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: str = Field(foreign_key="orders.order_id")
    name: str
    quantity: int
    price_vnd: int

    order: Optional["OrderTable"] = Relationship(back_populates="items")


class OrderTable(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: str = Field(primary_key=True)
    customer: str
    user_id: str
    status: str
    payment: str
    order_date: str
    estimated_delivery: Optional[str] = None
    delivered_date: Optional[str] = None
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    delivery_address: Optional[str] = None
    note: Optional[str] = None
    return_reason: Optional[str] = None
    return_status: Optional[str] = None
    refund_method: Optional[str] = None
    estimated_refund_date: Optional[str] = None
    cancellation_reason: Optional[str] = None
    refund_status: Optional[str] = None

    items: List[OrderItemTable] = Relationship(
        back_populates="order", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class TransactionTable(SQLModel, table=True):
    __tablename__ = "transactions"

    transaction_id: str = Field(primary_key=True)
    user_id: str
    amount_vnd: int
    payment_method: str
    status: str
    timestamp: str
    linked_order: Optional[str] = None
    bank_reference: Optional[str] = None
    note: Optional[str] = None


class TicketTable(SQLModel, table=True):
    __tablename__ = "tickets"

    ticket_id: str = Field(primary_key=True)
    user_id: str
    user_name: Optional[str] = None
    issue: str
    priority: Optional[str] = None
    status: str = Field(default="open")
    assigned_to: Optional[str] = None
    created: Optional[str] = None
    created_at: Optional[str] = None
    last_update: Optional[str] = None
    resolution: Optional[str] = None
