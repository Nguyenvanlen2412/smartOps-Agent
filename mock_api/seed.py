# mock_api/seed.py
from sqlmodel import Session, select
from mock_api.models import UserTable, OrderTable, OrderItemTable, TransactionTable, TicketTable


def seed_initial_data(session: Session):
    """Seed sample data into SQLite if tables are empty."""
    # Check if data already exists
    existing_user = session.exec(select(UserTable)).first()
    if existing_user:
        return  # Database is already seeded

    # Seed Users
    users_data = [
        UserTable(user_id="U00421", name="Nguyen Van An", email="van.an@gmail.com"),
        UserTable(user_id="U00876", name="Tran Thi Bich", email="bich.tran@gmail.com"),
        UserTable(user_id="U01133", name="Pham Duc Minh", email="duc.minh@outlook.com"),
        UserTable(user_id="U00654", name="Le Ngoc Linh", email="ngoc.linh@yahoo.com"),
        UserTable(user_id="U00312", name="Hoang Thanh Tung", email="thanh.tung@gmail.com"),
        UserTable(user_id="U01245", name="Vu Hoang Long", email="hoanglong.vu@gmail.com"),
        UserTable(user_id="U00519", name="Do Thi Thao", email="thaodt99@yahoo.com"),
        UserTable(user_id="U00922", name="Nguyen Minh Triet", email="triet.nm@fpt.edu.vn"),
        UserTable(user_id="U00288", name="Dang Hoang Yen", email="hoangyen.dang@gmail.com"),
    ]
    session.add_all(users_data)

    # Seed Orders & Order Items
    orders_data = [
        (
            OrderTable(
                order_id="VN1024", customer="Nguyen Van An", user_id="U00421",
                status="In Transit", payment="VNPay QR – Paid", order_date="2025-05-18",
                estimated_delivery="2025-05-22", carrier="Giao Hang Nhanh (GHN)",
                tracking_number="GHN-88291047", delivery_address="45 Hoang Quoc Viet, Cau Giay, Hanoi"
            ),
            [OrderItemTable(name="Samsung Galaxy A55 5G", quantity=1, price_vnd=9490000)]
        ),
        (
            OrderTable(
                order_id="VN1025", customer="Tran Thi Bich", user_id="U00876",
                status="Delivered", payment="Cash on Delivery – Paid", order_date="2025-05-15",
                delivered_date="2025-05-17", carrier="Viettel Post", tracking_number="VTEL-44018833",
                delivery_address="12 Le Van Luong, Thanh Xuan, Hanoi"
            ),
            [OrderItemTable(name="Logitech MX Master 3S", quantity=1, price_vnd=2190000)]
        ),
        (
            OrderTable(
                order_id="VN1026", customer="Pham Duc Minh", user_id="U01133",
                status="Pending Payment", payment="Internet Banking – Awaiting Confirmation",
                order_date="2025-05-20", note="Payment not yet confirmed by bank. Order will auto-cancel after 24 hours if unpaid."
            ),
            [OrderItemTable(name="MacBook Air M3 13-inch", quantity=1, price_vnd=28990000)]
        ),
        (
            OrderTable(
                order_id="VN1027", customer="Le Ngoc Linh", user_id="U00654",
                status="Return Requested", payment="Credit Card", order_date="2025-05-19",
                return_reason="R01 – Defective upon arrival (left ear cup no sound)",
                return_status="Approved – Awaiting pickup", refund_method="Credit card reversal",
                estimated_refund_date="2025-05-27"
            ),
            [OrderItemTable(name="Sony WH-1000XM5 Headphones", quantity=1, price_vnd=7490000)]
        ),
        (
            OrderTable(
                order_id="VN1028", customer="Hoang Thanh Tung", user_id="U00312",
                status="Cancelled", payment="MoMo Wallet", order_date="2025-05-19",
                cancellation_reason="Customer requested cancellation within 1 hour of order",
                refund_status="Refunded to MoMo wallet on 2025-05-19"
            ),
            [OrderItemTable(name="Xiaomi Smart Band 9", quantity=1, price_vnd=890000)]
        ),
        (
            OrderTable(
                order_id="VN1029", customer="Vu Hoang Long", user_id="U01245",
                status="Processing", payment="Credit Card (Visa) – Paid", order_date="2025-05-21",
                estimated_delivery="2025-05-25", carrier="Ninja Van", tracking_number="NJV-99104822",
                delivery_address="182 Dien Bien Phu, Ward 7, District 3, Ho Chi Minh City"
            ),
            [
                OrderItemTable(name="ASUS ROG Zephyrus G14", quantity=1, price_vnd=34990000),
                OrderItemTable(name="Razer DeathAdder V3 Pro", quantity=1, price_vnd=3290000)
            ]
        ),
        (
            OrderTable(
                order_id="VN1030", customer="Do Thi Thao", user_id="U00519",
                status="Delayed", payment="ShopeePay – Paid", order_date="2025-05-14",
                estimated_delivery="2025-05-24", carrier="J&T Express", tracking_number="JT-77301982",
                delivery_address="88 Le Loi, Hai Chau District, Da Nang",
                note="Shipment held briefly at the Hanoi sorting hub due to weather delays."
            ),
            [OrderItemTable(name="Keychron Q1 Pro Mechanical Keyboard", quantity=1, price_vnd=4500000)]
        ),
        (
            OrderTable(
                order_id="VN1031", customer="Nguyen Minh Triet", user_id="U00922",
                status="Partially Refunded", payment="VNPay QR – Paid", order_date="2025-05-22",
                delivery_address="Room 402, Block B, Sunrise City, District 7, Ho Chi Minh City",
                note="Out of stock on Anker PowerBank; cables shipped successfully.",
                refund_status="2,100,000 VND returned to source account on 2025-05-23"
            ),
            [
                OrderItemTable(name="Anker PowerBank 24K", quantity=1, price_vnd=2100000),
                OrderItemTable(name="Apple Lightning Cable 1m", quantity=2, price_vnd=490000)
            ]
        ),
        (
            OrderTable(
                order_id="VN1032", customer="Dang Hoang Yen", user_id="U00288",
                status="Shipped", payment="Techcombank Financing / Installment – Approved",
                order_date="2025-05-22", estimated_delivery="2025-05-26",
                carrier="Giao Hang Tiet Kiem (GHTK)", tracking_number="GHTK-552019482",
                delivery_address="54 Tran Hung Dao, Ninh Kieu District, Can Tho"
            ),
            [OrderItemTable(name="iPad Air M2 11-inch", quantity=1, price_vnd=16990000)]
        ),
    ]

    for order_obj, items in orders_data:
        session.add(order_obj)
        for item in items:
            item.order_id = order_obj.order_id
            session.add(item)

    # Seed Transactions
    transactions_data = [
        TransactionTable(
            transaction_id="TXN-20250518-00421", user_id="U00421", amount_vnd=9490000,
            payment_method="VNPay QR", status="Success", timestamp="2025-05-18 14:32:07",
            linked_order="VN1024", bank_reference="VCB-REF-7731029"
        ),
        TransactionTable(
            transaction_id="TXN-20250520-01133", user_id="U01133", amount_vnd=28990000,
            payment_method="Internet Banking (Techcombank)", status="Pending",
            timestamp="2025-05-20 09:15:44", linked_order="VN1026", note="Awaiting bank confirmation webhook"
        ),
        TransactionTable(
            transaction_id="TXN-20250515-00876", user_id="U00876", amount_vnd=2190000,
            payment_method="Cash on Delivery", status="Collected by Driver",
            timestamp="2025-05-17 16:48:00", linked_order="VN1025"
        ),
        TransactionTable(
            transaction_id="TXN-20250519-00312", user_id="U00312", amount_vnd=890000,
            payment_method="MoMo", status="Refunded", timestamp="2025-05-19 10:02:33",
            linked_order="VN1028", note="Refunded on 2025-05-19 10:55:10"
        ),
        TransactionTable(
            transaction_id="TXN-20250521-01245", user_id="U01245", amount_vnd=38280000,
            payment_method="Credit Card (Visa/VNPay Gate)", status="Success",
            timestamp="2025-05-21 19:45:12", linked_order="VN1029", bank_reference="VCB-REF-9982415"
        ),
        TransactionTable(
            transaction_id="TXN-20250514-00519", user_id="U00519", amount_vnd=4500000,
            payment_method="ShopeePay Wallet", status="Success",
            timestamp="2025-05-14 11:20:05", linked_order="VN1030", bank_reference="SPP-7710294-MP"
        ),
        TransactionTable(
            transaction_id="TXN-20250522-00922", user_id="U00922", amount_vnd=3080000,
            payment_method="VNPay QR", status="Partially Refunded",
            timestamp="2025-05-22 08:14:22", linked_order="VN1031", bank_reference="VNP-RFD-882104",
            note="Refunded on 2025-05-23 10:00:15"
        ),
        TransactionTable(
            transaction_id="TXN-20250522-00288", user_id="U00288", amount_vnd=16990000,
            payment_method="Techcombank Installment Pay", status="Success",
            timestamp="2025-05-22 15:30:00", linked_order="VN1032", bank_reference="TCB-INS-002914"
        ),
    ]
    session.add_all(transactions_data)

    # Seed Tickets
    tickets_data = [
        TicketTable(
            ticket_id="TKT-0881", user_id="U00654", user_name="Le Ngoc Linh",
            issue="Defective headphones – left ear cup silent", priority="High",
            status="In Progress", assigned_to="Nguyen Thi Mai", created="2025-05-19 08:30:00",
            created_at="2025-05-19T08:30:00", last_update="2025-05-20",
            resolution="Return approved, pickup scheduled for 2025-05-22"
        ),
        TicketTable(
            ticket_id="TKT-0882", user_id="U00421", user_name="Nguyen Van An",
            issue="Wants to know delivery ETA for order VN1024", priority="Low",
            status="Resolved via chatbot", assigned_to="Chatbot", created="2025-05-20 11:05:00",
            created_at="2025-05-20T11:05:00", last_update="2025-05-20",
            resolution="Chatbot confirmed delivery by 2025-05-22 via GHN tracking"
        ),
        TicketTable(
            ticket_id="TKT-0883", user_id="U00519", user_name="Do Thi Thao",
            issue="Order VN1030 past original delivery estimate", priority="Medium",
            status="Resolved", assigned_to="Tran Van Binh", created="2025-05-20 14:15:00",
            created_at="2025-05-20T14:15:00", last_update="2025-05-20",
            resolution="Contacted J&T Express hub. Confirmed logistics bottleneck cleared; updated status to Delayed with new ETA of 2025-05-24."
        ),
        TicketTable(
            ticket_id="TKT-0884", user_id="U00922", user_name="Nguyen Minh Triet",
            issue="Inquiry about missing item refund timeline for VN1031", priority="Medium",
            status="Closed", assigned_to="Nguyen Thi Mai", created="2025-05-23 09:12:00",
            created_at="2025-05-23T09:12:00", last_update="2025-05-23",
            resolution="System verified the 2,100,000 VND partial refund transaction initiated. Provided bank transaction ID to client."
        ),
        TicketTable(
            ticket_id="TKT-0885", user_id="U01245", user_name="Vu Hoang Long",
            issue="Requests change of delivery address for VN1029 before shipping", priority="High",
            status="Open", assigned_to=None, created="2025-05-21 20:05:00",
            created_at="2025-05-21T20:05:00", last_update="2025-05-21"
        ),
    ]
    session.add_all(tickets_data)

    session.commit()
