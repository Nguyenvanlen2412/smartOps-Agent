# mock_api/mock_db.py
# TechShop Vietnam Mock Database
# Sample data mimicking techshop_sample_data.md format

ORDERS = {
    "VN1024": {
        "order_id": "VN1024",
        "customer": "Nguyen Van An",
        "user_id": "U00421",
        "status": "In Transit",
        "items": [
            {"name": "Samsung Galaxy A55 5G", "quantity": 1, "price_vnd": 9490000}
        ],
        "payment": "VNPay QR – Paid",
        "order_date": "2025-05-18",
        "estimated_delivery": "2025-05-22",
        "carrier": "Giao Hang Nhanh (GHN)",
        "tracking_number": "GHN-88291047",
        "delivery_address": "45 Hoang Quoc Viet, Cau Giay, Hanoi"
    },
    "VN1025": {
        "order_id": "VN1025",
        "customer": "Tran Thi Bich",
        "user_id": "U00876",
        "status": "Delivered",
        "items": [
            {"name": "Logitech MX Master 3S", "quantity": 1, "price_vnd": 2190000}
        ],
        "payment": "Cash on Delivery – Paid",
        "order_date": "2025-05-15",
        "delivered_date": "2025-05-17",
        "carrier": "Viettel Post",
        "tracking_number": "VTEL-44018833",
        "delivery_address": "12 Le Van Luong, Thanh Xuan, Hanoi"
    },
    "VN1026": {
        "order_id": "VN1026",
        "customer": "Pham Duc Minh",
        "user_id": "U01133",
        "status": "Pending Payment",
        "items": [
            {"name": "MacBook Air M3 13-inch", "quantity": 1, "price_vnd": 28990000}
        ],
        "payment": "Internet Banking – Awaiting Confirmation",
        "order_date": "2025-05-20",
        "note": "Payment not yet confirmed by bank. Order will auto-cancel after 24 hours if unpaid."
    },
    "VN1027": {
        "order_id": "VN1027",
        "customer": "Le Ngoc Linh",
        "user_id": "U00654",
        "status": "Return Requested",
        "items": [
            {"name": "Sony WH-1000XM5 Headphones", "quantity": 1, "price_vnd": 7490000}
        ],
        "payment": "Credit Card",
        "order_date": "2025-05-19",
        "return_reason": "R01 – Defective upon arrival (left ear cup no sound)",
        "return_status": "Approved – Awaiting pickup",
        "refund_method": "Credit card reversal",
        "estimated_refund_date": "2025-05-27"
    },
    "VN1028": {
        "order_id": "VN1028",
        "customer": "Hoang Thanh Tung",
        "user_id": "U00312",
        "status": "Cancelled",
        "items": [
            {"name": "Xiaomi Smart Band 9", "quantity": 1, "price_vnd": 890000}
        ],
        "payment": "MoMo Wallet",
        "order_date": "2025-05-19",
        "cancellation_reason": "Customer requested cancellation within 1 hour of order",
        "refund_status": "Refunded to MoMo wallet on 2025-05-19"
    }
}

TRANSACTIONS = {
    "TXN-20250518-00421": {
        "transaction_id": "TXN-20250518-00421",
        "user_id": "U00421",
        "amount_vnd": 9490000,
        "payment_method": "VNPay QR",
        "status": "Success",
        "timestamp": "2025-05-18 14:32:07",
        "linked_order": "VN1024",
        "bank_reference": "VCB-REF-7731029"
    },
    "TXN-20250520-01133": {
        "transaction_id": "TXN-20250520-01133",
        "user_id": "U01133",
        "amount_vnd": 28990000,
        "payment_method": "Internet Banking (Techcombank)",
        "status": "Pending",
        "timestamp": "2025-05-20 09:15:44",
        "linked_order": "VN1026",
        "note": "Awaiting bank confirmation webhook"
    },
    "TXN-20250515-00876": {
        "transaction_id": "TXN-20250515-00876",
        "user_id": "U00876",
        "amount_vnd": 2190000,
        "payment_method": "Cash on Delivery",
        "status": "Collected by Driver",
        "timestamp": "2025-05-17 16:48:00",
        "linked_order": "VN1025"
    },
    "TXN-20250519-00312": {
        "transaction_id": "TXN-20250519-00312",
        "user_id": "U00312",
        "amount_vnd": 890000,
        "payment_method": "MoMo",
        "status": "Refunded",
        "timestamp": "2025-05-19 10:02:33",
        "linked_order": "VN1028",
        "note": "Refunded on 2025-05-19 10:55:10"
    }
}

TICKETS = {
    "TKT-0881": {
        "ticket_id": "TKT-0881",
        "user_id": "U00654",
        "user_name": "Le Ngoc Linh",
        "issue": "Defective headphones – left ear cup silent",
        "priority": "High",
        "status": "In Progress",
        "assigned_to": "Nguyen Thi Mai",
        "created": "2025-05-19 08:30:00",
        "last_update": "2025-05-20",
        "resolution": "Return approved, pickup scheduled for 2025-05-22"
    },
    "TKT-0882": {
        "ticket_id": "TKT-0882",
        "user_id": "U00421",
        "user_name": "Nguyen Van An",
        "issue": "Wants to know delivery ETA for order VN1024",
        "priority": "Low",
        "status": "Resolved via chatbot",
        "assigned_to": "Chatbot",
        "created": "2025-05-20 11:05:00",
        "last_update": "2025-05-20",
        "resolution": "Chatbot confirmed delivery by 2025-05-22 via GHN tracking"
    }
}


USERS = {
    "U00421": {"name": "Nguyen Van An",  "email": "van.an@gmail.com"},
    "U00876": {"name": "Tran Thi Bich",  "email": "bich.tran@gmail.com"},
    "U01133": {"name": "Pham Duc Minh",  "email": "duc.minh@outlook.com"},
    "U00654": {"name": "Le Ngoc Linh",   "email": "ngoc.linh@yahoo.com"},
    "U00312": {"name": "Hoang Thanh Tung","email": "thanh.tung@gmail.com"},
}