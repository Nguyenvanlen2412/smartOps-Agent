# mock_api/mock_db.py
from pydantic import BaseModel
from typing import Optional


class OrderItem(BaseModel):
    name: str
    quantity: int
    price_vnd: int


class Order(BaseModel):
    order_id: str
    customer: str
    user_id: str
    status: str
    items: list[OrderItem]
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


class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    amount_vnd: int
    payment_method: str
    status: str
    timestamp: str
    linked_order: Optional[str] = None
    bank_reference: Optional[str] = None
    note: Optional[str] = None


class Ticket(BaseModel):
    ticket_id: str
    user_id: str
    user_name: Optional[str] = None
    issue: str
    priority: Optional[str] = None
    status: str
    assigned_to: Optional[str] = None
    created: Optional[str] = None
    created_at: Optional[str] = None
    last_update: Optional[str] = None
    resolution: Optional[str] = None


class User(BaseModel):
    name: str
    email: str


# ── Typed Data ──────────────────────────────────────────────

ORDERS: dict[str, Order] = {
    "VN1024": Order(
        order_id="VN1024", customer="Nguyen Van An", user_id="U00421",
        status="In Transit",
        items=[OrderItem(name="Samsung Galaxy A55 5G", quantity=1, price_vnd=9490000)],
        payment="VNPay QR – Paid", order_date="2025-05-18",
        estimated_delivery="2025-05-22", carrier="Giao Hang Nhanh (GHN)",
        tracking_number="GHN-88291047",
        delivery_address="45 Hoang Quoc Viet, Cau Giay, Hanoi",
    ),
    "VN1025": Order(
        order_id="VN1025", customer="Tran Thi Bich", user_id="U00876",
        status="Delivered",
        items=[OrderItem(name="Logitech MX Master 3S", quantity=1, price_vnd=2190000)],
        payment="Cash on Delivery – Paid", order_date="2025-05-15",
        delivered_date="2025-05-17", carrier="Viettel Post",
        tracking_number="VTEL-44018833",
        delivery_address="12 Le Van Luong, Thanh Xuan, Hanoi",
    ),
    "VN1026": Order(
        order_id="VN1026", customer="Pham Duc Minh", user_id="U01133",
        status="Pending Payment",
        items=[OrderItem(name="MacBook Air M3 13-inch", quantity=1, price_vnd=28990000)],
        payment="Internet Banking – Awaiting Confirmation", order_date="2025-05-20",
        note="Payment not yet confirmed by bank. Order will auto-cancel after 24 hours if unpaid.",
    ),
    "VN1027": Order(
        order_id="VN1027", customer="Le Ngoc Linh", user_id="U00654",
        status="Return Requested",
        items=[OrderItem(name="Sony WH-1000XM5 Headphones", quantity=1, price_vnd=7490000)],
        payment="Credit Card", order_date="2025-05-19",
        return_reason="R01 – Defective upon arrival (left ear cup no sound)",
        return_status="Approved – Awaiting pickup",
        refund_method="Credit card reversal", estimated_refund_date="2025-05-27",
    ),
    "VN1028": Order(
        order_id="VN1028", customer="Hoang Thanh Tung", user_id="U00312",
        status="Cancelled",
        items=[OrderItem(name="Xiaomi Smart Band 9", quantity=1, price_vnd=890000)],
        payment="MoMo Wallet", order_date="2025-05-19",
        cancellation_reason="Customer requested cancellation within 1 hour of order",
        refund_status="Refunded to MoMo wallet on 2025-05-19",
    ),
    "VN1029": Order(
        order_id="VN1029",
        customer="Vu Hoang Long",
        user_id="U01245",
        status="Processing",
        items=[
            OrderItem(name="ASUS ROG Zephyrus G14", quantity=1, price_vnd=34990000),
            OrderItem(name="Razer DeathAdder V3 Pro", quantity=1, price_vnd=3290000),
        ],
        payment="Credit Card (Visa) – Paid",
        order_date="2025-05-21",
        estimated_delivery="2025-05-25",
        carrier="Ninja Van",
        tracking_number="NJV-99104822",
        delivery_address="182 Dien Bien Phu, Ward 7, District 3, Ho Chi Minh City",
    ),
    "VN1030": Order(
        order_id="VN1030",
        customer="Do Thi Thao",
        user_id="U00519",
        status="Delayed",
        items=[
            OrderItem(name="Keychron Q1 Pro Mechanical Keyboard", quantity=1, price_vnd=4500000)
        ],
        payment="ShopeePay – Paid",
        order_date="2025-05-14",
        estimated_delivery="2025-05-24",
        carrier="J&T Express",
        tracking_number="JT-77301982",
        delivery_address="88 Le Loi, Hai Chau District, Da Nang",
        note="Shipment held briefly at the Hanoi sorting hub due to weather delays.",
    ),
    "VN1031": Order(
        order_id="VN1031",
        customer="Nguyen Minh Triet",
        user_id="U00922",
        status="Partially Refunded",
        items=[
            OrderItem(name="Anker PowerBank 24K", quantity=1, price_vnd=2100000),
            OrderItem(name="Apple Lightning Cable 1m", quantity=2, price_vnd=490000),
        ],
        payment="VNPay QR – Paid",
        order_date="2025-05-22",
        delivery_address="Room 402, Block B, Sunrise City, District 7, Ho Chi Minh City",
        note="Out of stock on Anker PowerBank; cables shipped successfully.",
        refund_status="2,100,000 VND returned to source account on 2025-05-23",
    ),
    "VN1032": Order(
        order_id="VN1032",
        customer="Dang Hoang Yen",
        user_id="U00288",
        status="Shipped",
        items=[
            OrderItem(name="iPad Air M2 11-inch", quantity=1, price_vnd=16990000)
        ],
        payment="Techcombank Financing / Installment – Approved",
        order_date="2025-05-22",
        estimated_delivery="2025-05-26",
        carrier="Giao Hang Tiet Kiem (GHTK)",
        tracking_number="GHTK-552019482",
        delivery_address="54 Tran Hung Dao, Ninh Kieu District, Can Tho",
    ),
}

TRANSACTIONS: dict[str, Transaction] = {
    "TXN-20250518-00421": Transaction(
        transaction_id="TXN-20250518-00421", user_id="U00421",
        amount_vnd=9490000, payment_method="VNPay QR", status="Success",
        timestamp="2025-05-18 14:32:07", linked_order="VN1024",
        bank_reference="VCB-REF-7731029",
    ),
    "TXN-20250520-01133": Transaction(
        transaction_id="TXN-20250520-01133", user_id="U01133",
        amount_vnd=28990000, payment_method="Internet Banking (Techcombank)",
        status="Pending", timestamp="2025-05-20 09:15:44", linked_order="VN1026",
        note="Awaiting bank confirmation webhook",
    ),
    "TXN-20250515-00876": Transaction(
        transaction_id="TXN-20250515-00876", user_id="U00876",
        amount_vnd=2190000, payment_method="Cash on Delivery",
        status="Collected by Driver", timestamp="2025-05-17 16:48:00",
        linked_order="VN1025",
    ),
    "TXN-20250519-00312": Transaction(
        transaction_id="TXN-20250519-00312", user_id="U00312",
        amount_vnd=890000, payment_method="MoMo", status="Refunded",
        timestamp="2025-05-19 10:02:33", linked_order="VN1028",
        note="Refunded on 2025-05-19 10:55:10",
    ),
    "TXN-20250521-01245": Transaction(
        transaction_id="TXN-20250521-01245",
        user_id="U01245",
        amount_vnd=38280000,
        payment_method="Credit Card (Visa/VNPay Gate)",
        status="Success",
        timestamp="2025-05-21 19:45:12",
        linked_order="VN1029",
        bank_reference="VCB-REF-9982415",
    ),
    "TXN-20250514-00519": Transaction(
        transaction_id="TXN-20250514-00519",
        user_id="U00519",
        amount_vnd=4500000,
        payment_method="ShopeePay Wallet",
        status="Success",
        timestamp="2025-05-14 11:20:05",
        linked_order="VN1030",
        bank_reference="SPP-7710294-MP",
    ),
    "TXN-20250522-00922": Transaction(
        transaction_id="TXN-20250522-00922",
        user_id="U00922",
        amount_vnd=3080000,
        payment_method="VNPay QR",
        status="Partially Refunded",
        timestamp="2025-05-22 08:14:22",
        linked_order="VN1031",
        bank_reference="VNP-RFD-882104",
        note="Refunded on 2025-05-23 10:00:15",
    ),
    "TXN-20250522-00288": Transaction(
        transaction_id="TXN-20250522-00288",
        user_id="U00288",
        amount_vnd=16990000,
        payment_method="Techcombank Installment Pay",
        status="Success",
        timestamp="2025-05-22 15:30:00",
        linked_order="VN1032",
        bank_reference="TCB-INS-002914",
    ),

}

TICKETS: dict[str, Ticket] = {
    "TKT-0881": Ticket(
        ticket_id="TKT-0881", user_id="U00654", user_name="Le Ngoc Linh",
        issue="Defective headphones – left ear cup silent", priority="High",
        status="In Progress", assigned_to="Nguyen Thi Mai",
        created="2025-05-19 08:30:00", last_update="2025-05-20",
        resolution="Return approved, pickup scheduled for 2025-05-22",
    ),
    "TKT-0882": Ticket(
        ticket_id="TKT-0882", user_id="U00421", user_name="Nguyen Van An",
        issue="Wants to know delivery ETA for order VN1024", priority="Low",
        status="Resolved via chatbot", assigned_to="Chatbot",
        created="2025-05-20 11:05:00", last_update="2025-05-20",
        resolution="Chatbot confirmed delivery by 2025-05-22 via GHN tracking",
    ),
    "TKT-0883": Ticket(
        ticket_id="TKT-0883",
        user_id="U00519",
        user_name="Do Thi Thao",
        issue="Order VN1030 past original delivery estimate",
        priority="Medium",
        status="Resolved",
        assigned_to="Tran Van Binh",
        created="2025-05-20 14:15:00",
        last_update="2025-05-20",
        resolution="Contacted J&T Express hub. Confirmed logistics bottleneck cleared; updated system status to 'Delayed' with new ETA of 2025-05-24. Customer notified via SMS.",
    ),
    "TKT-0884": Ticket(
        ticket_id="TKT-0884",
        user_id="U00922",
        user_name="Nguyen Minh Triet",
        issue="Inquiry about missing item refund timeline for VN1031",
        priority="Medium",
        status="Closed",
        assigned_to="Nguyen Thi Mai",
        created="2025-05-23 09:12:00",
        last_update="2025-05-23",
        resolution="System verified the 2,100,000 VND partial refund transaction initiated at 10:00:15. Provided bank transaction ID to client.",
    ),
    "TKT-0885": Ticket(
        ticket_id="TKT-0885",
        user_id="U01245",
        user_name="Vu Hoang Long",
        issue="Requests change of delivery address for VN1029 before shipping",
        priority="High",
        status="Open",
        assigned_to=None,
        created="2025-05-21 20:05:00",
        last_update="2025-05-21",
        note="Customer wants to route the package to his office address instead of his home address. Package still in 'Processing' queue.",
    ),
}

USERS: dict[str, User] = {
    "U00421": User(name="Nguyen Van An", email="van.an@gmail.com"),
    "U00876": User(name="Tran Thi Bich", email="bich.tran@gmail.com"),
    "U01133": User(name="Pham Duc Minh", email="duc.minh@outlook.com"),
    "U00654": User(name="Le Ngoc Linh", email="ngoc.linh@yahoo.com"),
    "U00312": User(name="Hoang Thanh Tung", email="thanh.tung@gmail.com"),
    "U01245": User(name="Vu Hoang Long", email="hoanglong.vu@gmail.com"),
    "U00519": User(name="Do Thi Thao", email="thaodt99@yahoo.com"),
    "U00922": User(name="Nguyen Minh Triet", email="triet.nm@fpt.edu.vn"),
    "U00288": User(name="Dang Hoang Yen", email="hoangyen.dang@gmail.com"),
}