# TechShop Vietnam – Sample Order & Transaction Data

> This document simulates internal order/transaction records used for agent tool-calling tests.
> In production, this data would be fetched live from a database via API.

---

## Sample Orders

### Order 
- **Id**VN1024
- **Customer:** Nguyen Van An (user_id: U00421)
- **Status:** In Transit
- **Items:** Samsung Galaxy A55 5G (x1) – 9,490,000 VND
- **Payment:** VNPay QR – Paid
- **Order Date:** 2025-05-18
- **Estimated Delivery:** 2025-05-22
- **Carrier:** Giao Hang Nhanh (GHN) | Tracking: GHN-88291047
- **Delivery Address:** 45 Hoang Quoc Viet, Cau Giay, Hanoi

---

### Order 
- **Id**VN1025
- **Customer:** Tran Thi Bich (user_id: U00876)
- **Status:** Delivered
- **Items:** Logitech MX Master 3S (x1) – 2,190,000 VND
- **Payment:** Cash on Delivery – Paid
- **Order Date:** 2025-05-15
- **Delivered Date:** 2025-05-17
- **Carrier:** Viettel Post | Tracking: VTEL-44018833
- **Delivery Address:** 12 Le Van Luong, Thanh Xuan, Hanoi

---

### Order 
- **Id**VN1026
- **Customer:** Pham Duc Minh (user_id: U01133)
- **Status:** Pending Payment
- **Items:** MacBook Air M3 13-inch (x1) – 28,990,000 VND
- **Payment:** Internet Banking – Awaiting Confirmation
- **Order Date:** 2025-05-20
- **Note:** Payment not yet confirmed by bank. Order will auto-cancel after 24 hours if unpaid.

---

### Order 
- **Id**VN1027
- **Customer:** Le Ngoc Linh (user_id: U00654)
- **Status:** Return Requested
- **Items:** Sony WH-1000XM5 Headphones (x1) – 7,490,000 VND
- **Return Reason:** R01 – Defective upon arrival (left ear cup no sound)
- **Return Status:** Approved – Awaiting pickup
- **Refund Method:** Credit card reversal
- **Estimated Refund Date:** 2025-05-27

---

### Order 
- **Id**VN1028
- **Customer:** Hoang Thanh Tung (user_id: U00312)
- **Status:** Cancelled
- **Items:** Xiaomi Smart Band 9 (x1) – 890,000 VND
- **Cancellation Reason:** Customer requested cancellation within 1 hour of order
- **Refund Status:** Refunded to MoMo wallet on 2025-05-19
- **Order Date:** 2025-05-19

---

### Order 
- **Id:** VN1029
- **Customer:** Vu Hoang Long (user_id: U01245)
- **Status:** Processing
- **Items:** 
  - ASUS ROG Zephyrus G14 (x1) – 34,990,000 VND
  - Razer DeathAdder V3 Pro (x1) – 3,290,000 VND
- **Payment:** Credit Card (Visa) – Paid
- **Order Date:** 2025-05-21
- **Estimated Delivery:** 2025-05-25
- **Carrier:** Ninja Van | Tracking: NJV-99104822
- **Delivery Address:** 182 Dien Bien Phu, Ward 7, District 3, Ho Chi Minh City

---

### Order 
- **Id:** VN1030
- **Customer:** Do Thi Thao (user_id: U00519)
- **Status:** Delayed
- **Items:** Keychron Q1 Pro Mechanical Keyboard (x1) – 4,500,000 VND
- **Payment:** ShopeePay – Paid
- **Order Date:** 2025-05-14
- **Original ETA:** 2025-05-18
- **New Estimated Delivery:** 2025-05-24
- **Carrier:** J&T Express | Tracking: JT-77301982
- **Note:** Shipment held briefly at the Hanoi sorting hub due to weather delays.
- **Delivery Address:** 88 Le Loi, Hai Chau District, Da Nang

---

### Order 
- **Id:** VN1031
- **Customer:** Nguyen Minh Triet (user_id: U00922)
- **Status:** Partially Refunded
- **Items:** 
  - Anker PowerBank 24K (x1) – 2,100,000 VND
  - Apple Lightning Cable 1m (x2) – 980,000 VND (490,000 VND each)
- **Payment:** VNPay QR – Paid
- **Order Date:** 2025-05-22
- **Return Reason:** Out of stock on Anker PowerBank; cables shipped successfully.
- **Refund Status:** 2,100,000 VND returned to source account on 2025-05-23
- **Delivery Address:** Room 402, Block B, Sunrise City, District 7, Ho Chi Minh City

---

### Order 
- **Id:** VN1032
- **Customer:** Dang Hoang Yen (user_id: U00288)
- **Status:** Shipped
- **Items:** iPad Air M2 11-inch (x1) – 16,990,000 VND
- **Payment:** Techcombank Financing / Installment – Approved
- **Order Date:** 2025-05-22
- **Estimated Delivery:** 2025-05-26
- **Carrier:** Giao Hang Tiet Kiem (GHTK) | Tracking: GHTK-552019482
- **Delivery Address:** 54 Tran Hung Dao, Ninh Kieu District, Can Tho

---

## Sample Transactions (VNPay)

### Transaction 
- **Id**TXN-20250518-00421
- **User:** U00421 (Nguyen Van An)
- **Amount:** 9,490,000 VND
- **Payment Method:** VNPay QR
- **Status:** Success
- **Timestamp:** 2025-05-18 14:32:07
- **Linked Order:** VN1024
- **Bank Reference:** VCB-REF-7731029

---

### Transaction 
- **Id**TXN-20250520-01133
- **User:** U01133 (Pham Duc Minh)
- **Amount:** 28,990,000 VND
- **Payment Method:** Internet Banking (Techcombank)
- **Status:** Pending
- **Timestamp:** 2025-05-20 09:15:44
- **Linked Order:** VN1026
- **Note:** Awaiting bank confirmation webhook

---

### Transaction 
- **Id**TXN-20250515-00876
- **User:** U00876 (Tran Thi Bich)
- **Amount:** 2,190,000 VND
- **Payment Method:** Cash on Delivery
- **Status:** Collected by Driver
- **Timestamp:** 2025-05-17 16:48:00
- **Linked Order:** VN1025

---

### Transaction 
- **Id**TXN-20250519-00312
- **User:** U00312 (Hoang Thanh Tung)
- **Amount:** 890,000 VND
- **Payment Method:** MoMo
- **Status:** Refunded
- **Original Timestamp:** 2025-05-19 10:02:33
- **Refund Timestamp:** 2025-05-19 10:55:10
- **Linked Order:** VN1028

---

### Transaction 
- **Id:** TXN-20250521-01245
- **User:** U01245 (Vu Hoang Long)
- **Amount:** 38,280,000 VND
- **Payment Method:** Credit Card (Visa/VNPay Gate)
- **Status:** Success
- **Timestamp:** 2025-05-21 19:45:12
- **Linked Order:** VN1029
- **Bank Reference:** VCB-REF-9982415

---

### Transaction 
- **Id:** TXN-20250514-00519
- **User:** U00519 (Do Thi Thao)
- **Amount:** 4,500,000 VND
- **Payment Method:** ShopeePay Wallet
- **Status:** Success
- **Timestamp:** 2025-05-14 11:20:05
- **Linked Order:** VN1030
- **Bank Reference:** SPP-7710294-MP

---

### Transaction 
- **Id:** TXN-20250522-00922
- **User:** U00922 (Nguyen Minh Triet)
- **Amount:** 3,080,000 VND
- **Payment Method:** VNPay QR
- **Status:** Partially Refunded
- **Original Timestamp:** 2025-05-22 08:14:22
- **Refund Timestamp:** 2025-05-23 10:00:15
- **Linked Order:** VN1031
- **Refund Reference:** VNP-RFD-882104

---

### Transaction 
- **Id:** TXN-20250522-00288
- **User:** U00288 (Dang Hoang Yen)
- **Amount:** 16,990,000 VND
- **Payment Method:** Techcombank Installment Pay
- **Status:** Success
- **Timestamp:** 2025-05-22 15:30:00
- **Linked Order:** VN1032
- **Bank Reference:** TCB-INS-002914

---

## Support Tickets

### Ticket 
- **Id**TKT-0881
- **User:** U00654 (Le Ngoc Linh)
- **Issue:** Defective headphones – left ear cup silent
- **Priority:** High
- **Status:** In Progress
- **Assigned To:** Support Agent – Nguyen Thi Mai
- **Created:** 2025-05-19 08:30:00
- **Last Update:** 2025-05-20 – Return approved, pickup scheduled for 2025-05-22

---

### Ticket 
- **Id**TKT-0882
- **User:** U00421 (Nguyen Van An)
- **Issue:** Wants to know delivery ETA for order VN1024
- **Priority:** Low
- **Status:** Resolved via chatbot
- **Created:** 2025-05-20 11:05:00
- **Resolution:** Chatbot confirmed delivery by 2025-05-22 via GHN tracking

---

### Ticket 
- **Id:** TKT-0883
- **User:** U00519 (Do Thi Thao)
- **Issue:** Order VN1030 past original delivery estimate
- **Priority:** Medium
- **Status:** Resolved
- **Assigned To:** Support Agent – Tran Van Binh
- **Created:** 2025-05-20 14:15:00
- **Resolution:** Contacted J&T Express hub. Confirmed logistics bottleneck cleared; updated system status to "Delayed" with new ETA of 2025-05-24. Customer notified via SMS.

---

### Ticket 
- **Id:** TKT-0884
- **User:** U00922 (Nguyen Minh Triet)
- **Issue:** Inquiry about missing item refund timeline for VN1031
- **Priority:** Medium
- **Status:** Closed
- **Assigned To:** Support Agent – Nguyen Thi Mai
- **Created:** 2025-05-23 09:12:00
- **Resolution:** System verified the 2,100,000 VND partial refund transaction initiated at 10:00:15. Provided bank transaction ID to client.

---

### Ticket 
- **Id:** TKT-0885
- **User:** U01245 (Vu Hoang Long)
- **Issue:** Requests change of delivery address for VN1029 before shipping
- **Priority:** High
- **Status:** Open
- **Assigned To:** Unassigned
- **Created:** 2025-05-21 20:05:00
- **Last Update:** Customer wants to route the package to his office address instead of his home address. Package still in "Processing" queue.

*This file is for development and testing purposes only.*
*TechShop Vietnam | Internal Use | May 2025*
