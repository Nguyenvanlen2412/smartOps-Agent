# TechShop Vietnam – Sample Order & Transaction Data

> This document simulates internal order/transaction records used for agent tool-calling tests.
> In production, this data would be fetched live from a database via API.

---

## Sample Orders

### Order #VN1024
- **Customer:** Nguyen Van An (user_id: U00421)
- **Status:** In Transit
- **Items:** Samsung Galaxy A55 5G (x1) – 9,490,000 VND
- **Payment:** VNPay QR – Paid
- **Order Date:** 2025-05-18
- **Estimated Delivery:** 2025-05-22
- **Carrier:** Giao Hang Nhanh (GHN) | Tracking: GHN-88291047
- **Delivery Address:** 45 Hoang Quoc Viet, Cau Giay, Hanoi

---

### Order #VN1025
- **Customer:** Tran Thi Bich (user_id: U00876)
- **Status:** Delivered
- **Items:** Logitech MX Master 3S (x1) – 2,190,000 VND
- **Payment:** Cash on Delivery – Paid
- **Order Date:** 2025-05-15
- **Delivered Date:** 2025-05-17
- **Carrier:** Viettel Post | Tracking: VTEL-44018833
- **Delivery Address:** 12 Le Van Luong, Thanh Xuan, Hanoi

---

### Order #VN1026
- **Customer:** Pham Duc Minh (user_id: U01133)
- **Status:** Pending Payment
- **Items:** MacBook Air M3 13-inch (x1) – 28,990,000 VND
- **Payment:** Internet Banking – Awaiting Confirmation
- **Order Date:** 2025-05-20
- **Note:** Payment not yet confirmed by bank. Order will auto-cancel after 24 hours if unpaid.

---

### Order #VN1027
- **Customer:** Le Ngoc Linh (user_id: U00654)
- **Status:** Return Requested
- **Items:** Sony WH-1000XM5 Headphones (x1) – 7,490,000 VND
- **Return Reason:** R01 – Defective upon arrival (left ear cup no sound)
- **Return Status:** Approved – Awaiting pickup
- **Refund Method:** Credit card reversal
- **Estimated Refund Date:** 2025-05-27

---

### Order #VN1028
- **Customer:** Hoang Thanh Tung (user_id: U00312)
- **Status:** Cancelled
- **Items:** Xiaomi Smart Band 9 (x1) – 890,000 VND
- **Cancellation Reason:** Customer requested cancellation within 1 hour of order
- **Refund Status:** Refunded to MoMo wallet on 2025-05-19
- **Order Date:** 2025-05-19

---

## Sample Transactions (VNPay)

### Transaction #TXN-20250518-00421
- **User:** U00421 (Nguyen Van An)
- **Amount:** 9,490,000 VND
- **Payment Method:** VNPay QR
- **Status:** Success
- **Timestamp:** 2025-05-18 14:32:07
- **Linked Order:** VN1024
- **Bank Reference:** VCB-REF-7731029

---

### Transaction #TXN-20250520-01133
- **User:** U01133 (Pham Duc Minh)
- **Amount:** 28,990,000 VND
- **Payment Method:** Internet Banking (Techcombank)
- **Status:** Pending
- **Timestamp:** 2025-05-20 09:15:44
- **Linked Order:** VN1026
- **Note:** Awaiting bank confirmation webhook

---

### Transaction #TXN-20250515-00876
- **User:** U00876 (Tran Thi Bich)
- **Amount:** 2,190,000 VND
- **Payment Method:** Cash on Delivery
- **Status:** Collected by Driver
- **Timestamp:** 2025-05-17 16:48:00
- **Linked Order:** VN1025

---

### Transaction #TXN-20250519-00312
- **User:** U00312 (Hoang Thanh Tung)
- **Amount:** 890,000 VND
- **Payment Method:** MoMo
- **Status:** Refunded
- **Original Timestamp:** 2025-05-19 10:02:33
- **Refund Timestamp:** 2025-05-19 10:55:10
- **Linked Order:** VN1028

---

## Support Tickets

### Ticket #TKT-0881
- **User:** U00654 (Le Ngoc Linh)
- **Issue:** Defective headphones – left ear cup silent
- **Priority:** High
- **Status:** In Progress
- **Assigned To:** Support Agent – Nguyen Thi Mai
- **Created:** 2025-05-19 08:30:00
- **Last Update:** 2025-05-20 – Return approved, pickup scheduled for 2025-05-22

---

### Ticket #TKT-0882
- **User:** U00421 (Nguyen Van An)
- **Issue:** Wants to know delivery ETA for order VN1024
- **Priority:** Low
- **Status:** Resolved via chatbot
- **Created:** 2025-05-20 11:05:00
- **Resolution:** Chatbot confirmed delivery by 2025-05-22 via GHN tracking

---

*This file is for development and testing purposes only.*
*TechShop Vietnam | Internal Use | May 2025*
