# mock_api/generate_mock_data.py
import random
from datetime import datetime, timedelta
from sqlmodel import Session, select
from mock_api.database import init_db, engine
from mock_api.models import (
    UserTable, ProductTable, OrderTable, OrderItemTable, TransactionTable, TicketTable
)
from mock_api.seed import seed_initial_data

# Realistic data samples for generating Vietnamese e-commerce records
FIRST_NAMES = ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Huynh", "Vu", "Vo", "Dang", "Bui", "Do", "Hồ", "Ngo", "Duong", "Ly"]
MIDDLE_NAMES = ["Van", "Thi", "Duc", "Hoang", "Minh", "Ngoc", "Thanh", "Quang", "Huu", "Anh", "Quoc", "Phuong", "Gia", "Bao"]
LAST_NAMES = ["An", "Binh", "Cuong", "Dung", "Em", "Giang", "Hieu", "Khanh", "Linh", "Mai", "Nam", "Oanh", "Phong", "Quan", "Sơn", "Tuan", "Uyên", "Vinh", "Yen", "Khoa"]

DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "fpt.edu.vn", "techshop.vn", "vnn.vn"]

STREETS = [
    "Hoang Quoc Viet, Cau Giay", "Le Van Luong, Thanh Xuan", "Tran Hung Dao, Hoan Kiem",
    "Nguyen Huu Tho, District 7", "Dien Bien Phu, District 3", "Le Loi, District 1",
    "Nguyen Van Linh, Hai Chau", "Bach Dang, Hong Bang", "Tran Phu, Ninh Kieu",
    "Pham Van Dong, Thu Duc", "Vo Van Kiet, District 5", "Nguyen Thi Minh Khai, District 1"
]
CITIES = ["Hanoi", "Ho Chi Minh City", "Da Nang", "Can Tho", "Hai Phong", "Nha Trang", "Vung Tau"]

CARRIERS = ["Giao Hang Nhanh (GHN)", "Viettel Post", "Giao Hang Tiet Kiem (GHTK)", "Ninja Van", "J&T Express", "SPX Express"]

PRODUCTS_POOL = [
    # Mobile Phones
    ("iPhone 15 Pro Max 256GB", "Mobile Phones", 34990000, 25, "Apple A17 Pro chip, Titanium design, 48MP camera system, 6.7-inch Super Retina XDR.", 12),
    ("iPhone 15 128GB", "Mobile Phones", 19990000, 35, "Dynamic Island, 48MP Main camera, A16 Bionic chip, USB-C connector.", 12),
    ("Samsung Galaxy S24 Ultra", "Mobile Phones", 31990000, 20, "Snapdragon 8 Gen 3, Galaxy AI, 200MP camera, built-in S Pen.", 12),
    ("Samsung Galaxy Z Fold5 512GB", "Mobile Phones", 38990000, 10, "7.6-inch Main Screen, Snapdragon 8 Gen 2, Flex Hinge, Dual App Multitasking.", 12),
    ("Xiaomi 14 Ultra", "Mobile Phones", 26990000, 15, "Leica Quad Camera System, Snapdragon 8 Gen 3, WQHD+ AMOLED.", 12),
    ("Xiaomi Redmi Note 13 Pro+ 5G", "Mobile Phones", 9490000, 45, "200MP OIS camera, 120W HyperCharge, IP68 water resistance, Dimensity 7200 Ultra.", 12),
    ("OPPO Reno11 Pro 5G", "Mobile Phones", 11990000, 30, "Portrait Expert camera, 80W SUPERVOOC charging, 120Hz 3D Curved screen.", 12),
    ("Realme GT 6", "Mobile Phones", 13490000, 18, "Snapdragon 8s Gen 3, 6000 nits Ultra Bright Display, 120W charging.", 12),
    ("Google Pixel 8 Pro", "Mobile Phones", 22490000, 12, "Google Tensor G3, Super Actua display, Pro camera controls, 7 years updates.", 12),
    ("Asus ROG Phone 8 Pro", "Mobile Phones", 28990000, 8, "Snapdragon 8 Gen 3, 165Hz AMOLED, AniMe Vision LED matrix, AirTrigger controls.", 12),
    
    # Laptops
    ("MacBook Pro 14-inch M3 Pro", "Laptops", 49990000, 10, "Apple M3 Pro 11-core CPU, 14-core GPU, 18GB Unified Memory, 512GB SSD.", 12),
    ("MacBook Air M3 15-inch", "Laptops", 32990000, 16, "Apple M3 chip, 15.3-inch Liquid Retina display, 16GB RAM, 512GB SSD.", 12),
    ("Dell XPS 13 9340", "Laptops", 39990000, 8, "Intel Core Ultra 7 155H, 16GB LPDDR5x, 512GB SSD, FHD+ InfinityEdge.", 12),
    ("Dell Alienware m16 R2", "Laptops", 54990000, 5, "Intel Core Ultra 9 185H, RTX 4080 12GB, 32GB DDR5, 1TB SSD, 240Hz QHD+.", 24),
    ("Lenovo ThinkPad X1 Carbon Gen 12", "Laptops", 45990000, 7, "Intel Core Ultra 7, 32GB RAM, 1TB SSD, 2.8K OLED Display.", 24),
    ("Lenovo Legion Slim 5 16-inch", "Laptops", 31990000, 12, "AMD Ryzen 7 7840HS, RTX 4060, 16GB RAM, 512GB SSD, 165Hz WQXGA.", 24),
    ("Asus Zenbook 14 OLED", "Laptops", 24990000, 14, "Intel Core Ultra 5, 16GB RAM, 512GB SSD, 3K 120Hz OLED screen.", 24),
    ("Acer Predator Helios 16", "Laptops", 42990000, 6, "Intel Core i9-13900HX, RTX 4070, 32GB RAM, 1TB SSD gaming laptop.", 24),
    ("HP Spectre x360 14", "Laptops", 36990000, 9, "Intel Core Ultra 7, 2-in-1 convertible touchscreen, 16GB RAM, 1TB SSD, OLED.", 12),
    ("LG Gram Pro 16", "Laptops", 38990000, 11, "Super light 1.19kg chassis, Intel Core Ultra 7, 32GB RAM, 1TB SSD, 144Hz IPS.", 24),
    
    # Tablets
    ("iPad Pro 13-inch M4", "Tablets", 37990000, 8, "Ultra Retina XDR OLED, Apple M4 chip, 256GB Wi-Fi, Apple Pencil Pro support.", 12),
    ("iPad Air M2 11-inch", "Tablets", 16990000, 20, "Apple M2 chip, 11-inch Liquid Retina, Wi-Fi 128GB, Center Stage camera.", 12),
    ("Samsung Galaxy Tab S9 Ultra", "Tablets", 27990000, 9, "14.6-inch Dynamic AMOLED 2X, Snapdragon 8 Gen 2, S Pen included, IP68.", 12),
    ("Xiaomi Pad 6S Pro 12.4", "Tablets", 13990000, 25, "12.4-inch 3K 144Hz display, Snapdragon 8 Gen 2, 120W HyperCharge, 6 speakers.", 12),

    # Audio
    ("Sony WH-1000XM4 Headphones", "Audio", 5990000, 40, "HD Noise Canceling Processor QN1, 30-hour battery life, Multipoint connection.", 12),
    ("Sony WH-1000XM5 Headphones", "Audio", 7490000, 30, "Auto NC Optimizer, 8 microphones, Ultra-comfortable lightweight design.", 12),
    ("Apple AirPods Pro Gen 2 (USB-C)", "Audio", 5690000, 50, "Active Noise Cancellation, Adaptive Audio, MagSafe Charging Case.", 12),
    ("Apple AirPods Max", "Audio", 13190000, 15, "Apple-designed dynamic driver, Active Noise Cancellation, Spatial Audio.", 12),
    ("Bose QuietComfort Ultra Earbuds", "Audio", 6990000, 22, "Immersive Audio, CustomTune technology, World-class noise cancellation.", 12),
    ("Sennheiser Momentum 4 Wireless", "Audio", 7990000, 18, "60-hour battery life, audiophile-inspired sound quality, adaptive noise cancellation.", 24),
    ("JBL Charge 5 Bluetooth Speaker", "Audio", 3490000, 35, "JBL Original Pro Sound, IP67 waterproof and dustproof, 20 hours playtime.", 12),
    ("JBL Boombox 3 Wireless Speaker", "Audio", 10990000, 10, "Massive sound, deepest bass, IP67 dust/waterproof, 24 hours playback.", 12),
    ("Marshall Stanmore III", "Audio", 9490000, 12, "Iconic home Bluetooth speaker, wide soundstage, brass control knobs.", 12),

    # Wearables
    ("Apple Watch Series 9 GPS 45mm", "Wearables", 10490000, 25, "S9 SiP chip, Double Tap gesture, brighter display, Blood Oxygen sensor.", 12),
    ("Apple Watch Ultra 2 GPS + Cellular", "Wearables", 21990000, 12, "49mm Titanium case, Precision dual-frequency GPS, 36-hour battery, 100m water resistance.", 12),
    ("Garmin Forerunner 265", "Wearables", 11690000, 15, "Running smartwatch with AMOLED display, training readiness, multi-band GPS.", 12),
    ("Garmin Fenix 7 Pro Sapphire Solar", "Wearables", 22990000, 8, "Solar charging lens, built-in LED flashlight, endurance score, Hill score.", 24),
    ("Samsung Galaxy Watch6 Classic", "Wearables", 7990000, 20, "Rotating bezel, Personalized HR Zone, Sleep coaching, Sapphire crystal.", 12),

    # Gaming & Accessories
    ("Sony PlayStation 5 Slim Digital", "Gaming Gear", 11990000, 15, "Custom AMD Zen 2 CPU, RDNA 2 GPU, 1TB ultra-fast SSD, DualSense haptics.", 12),
    ("Nintendo Switch OLED Model", "Gaming Gear", 7890000, 25, "7-inch OLED screen, wide adjustable stand, 64GB storage, wired LAN dock.", 12),
    ("ASUS ROG Ally X Handheld", "Gaming Gear", 23990000, 14, "AMD Ryzen Z1 Extreme, 24GB LPDDR5X RAM, 1TB SSD, 80Wh battery, Windows 11.", 24),
    ("Logitech G Pro X Superlight 2", "Gaming Gear", 3690000, 35, "LIGHTFORCE hybrid switches, HERO 2 sensor 32K DPI, 60g ultralight wireless.", 24),
    ("Razer DeathAdder V3 Pro Wireless", "Gaming Gear", 3290000, 30, "63g ergonomic lightweight mouse, Focus Pro 30K optical sensor.", 24),
    ("Keychron Q1 Max Custom Keyboard", "Gaming Gear", 4990000, 18, "Full aluminum body, 2.4GHz wireless + Bluetooth, Gateron Jupiter switches.", 12),
    ("SteelSeries Arctis Nova Pro Wireless", "Gaming Gear", 8990000, 12, "Dual Wireless audio system, Active Noise Cancellation, Infinity Power System.", 24),

    # Monitors
    ("LG UltraGear 27GP850-B 27-inch", "Monitors", 8990000, 15, "Nano IPS 1ms GTG, QHD (2560x1440), 180Hz overclocked, G-Sync compatible.", 24),
    ("LG Smart Monitor 32SQ700S 32-inch", "Monitors", 7490000, 20, "4K UHD IPS display, webOS smart TV features, 65W USB-C power delivery.", 24),
    ("Dell UltraSharp U2724D 27-inch", "Monitors", 9890000, 12, "IPS Black panel, 120Hz refresh rate, QHD, USB-C hub, 100% sRGB.", 36),
    ("ASUS ROG Swift OLED PG27AQDM", "Monitors", 22990000, 5, "27-inch QHD OLED, 240Hz, 0.03ms response time, custom heatsink.", 36),
    ("Samsung Odyssey G9 49-inch Curved", "Monitors", 29990000, 4, "Dual QHD (5120x1440) 1000R curved gaming monitor, 240Hz, 1ms, Quantum Mini-LED.", 24),

    # Computer Accessories & Power
    ("Anker 737 Power Bank 24,000mAh", "Computer Accessories", 2890000, 45, "140W bi-directional fast charging, smart digital display, 3 ports.", 18),
    ("SanDisk Extreme Portable SSD 2TB", "Computer Accessories", 4190000, 40, "Up to 1050MB/s read speed, IP65 water and dust resistance, NVMe speed.", 36),
    ("Samsung T7 Shield 1TB Portable SSD", "Computer Accessories", 2690000, 50, "Rugged rubber exterior, drop resistant up to 3m, IP65 water/dust resistant.", 36),
    ("Elgato Stream Deck MK.2", "Computer Accessories", 3890000, 22, "15 customizable LCD keys for controlling apps, livestreaming, and workflows.", 24),
    ("Logitech MX Master 3S Wireless Mouse", "Computer Accessories", 2190000, 40, "8K DPI track-on-glass sensor, Quiet Clicks, MagSpeed electromagnetic scrolling.", 12),

    # Smart Home & Cameras
    ("DJI Mini 4 Pro Drone (Fly More Combo)", "Cameras & Drones", 24990000, 8, "Under 249g, 4K/60fps HDR video, Omnidirectional obstacle sensing, 34-min flight.", 12),
    ("DJI Osmo Pocket 3 Gimbal Camera", "Cameras & Drones", 12990000, 15, "1-inch CMOS sensor, 4K/120fps, 2-inch rotatable touchscreen, 3-axis stabilization.", 12),
    ("Sony Alpha A7 IV Mirrorless Camera (Body)", "Cameras & Drones", 55990000, 6, "33MP full-frame Exmor R sensor, BIONZ XR engine, 4K 60p 10-bit video, Real-time Eye AF.", 24),
    ("Roborock S8 MaxV Ultra Robot Vacuum", "Smart Home", 29990000, 7, "10,000Pa suction power, All-in-One RockDock Ultra station, Reactive AI 2.0 obstacle avoidance.", 24),
]

ISSUE_TEMPLATES = [
    ("Package received damaged on delivery", "High"),
    ("Item missing from order shipment box", "High"),
    ("Screen flickers intermittently under load", "Medium"),
    ("Request tax invoice / VAT invoice issuance", "Low"),
    ("Cannot pair Bluetooth connection with phone", "Low"),
    ("Wrong color model delivered instead of ordered", "Medium"),
    ("Payment deducted twice on VNPay gateway", "Urgent"),
    ("Warranty repair claim for battery failure", "Medium"),
    ("Delivery status marked delivered but not received", "Urgent"),
    ("Inquiry about extended 2-year warranty terms", "Low")
]


def generate_flooded_data(target_users=50, target_orders=150, target_tickets=50):
    init_db()
    with Session(engine) as session:
        # Seed base data first if empty
        seed_initial_data(session)

        # 1. Generate Additional Users
        existing_users = session.exec(select(UserTable)).all()
        existing_ids = {u.user_id for u in existing_users}
        new_users = []
        
        user_id_counter = 100
        while len(existing_ids) < target_users + len(existing_users):
            uid = f"U00{user_id_counter}"
            user_id_counter += 1
            if uid in existing_ids:
                continue
            first = random.choice(FIRST_NAMES)
            mid = random.choice(MIDDLE_NAMES)
            last = random.choice(LAST_NAMES)
            full_name = f"{first} {mid} {last}"
            email_prefix = f"{first.lower()}.{last.lower()}{random.randint(10, 999)}"
            email = f"{email_prefix}@{random.choice(DOMAINS)}"
            
            user_obj = UserTable(user_id=uid, name=full_name, email=email)
            new_users.append(user_obj)
            existing_ids.add(uid)

        if new_users:
            session.add_all(new_users)
            session.commit()
            print(f"Added {len(new_users)} new users.")

        all_users = session.exec(select(UserTable)).all()

        # 2. Generate Additional Products
        existing_products = session.exec(select(ProductTable)).all()
        existing_prod_ids = {p.product_id for p in existing_products}
        new_products = []

        prod_counter = 9
        for p_name, p_cat, p_price, p_stock, p_desc, p_warr in PRODUCTS_POOL:
            pid = f"PROD-{prod_counter:03d}"
            prod_counter += 1
            if pid in existing_prod_ids:
                continue
            p_obj = ProductTable(
                product_id=pid,
                name=p_name,
                category=p_cat,
                price_vnd=p_price,
                stock_quantity=p_stock,
                description=p_desc,
                warranty_months=p_warr
            )
            new_products.append(p_obj)
            existing_prod_ids.add(pid)

        if new_products:
            session.add_all(new_products)
            session.commit()
            print(f"Added {len(new_products)} new products.")

        all_products = session.exec(select(ProductTable)).all()

        # 3. Generate Additional Orders & Order Items & Transactions
        existing_orders = session.exec(select(OrderTable)).all()
        order_counter = 1033
        existing_order_ids = {o.order_id for o in existing_orders}

        new_orders_count = 0
        new_txns_count = 0

        statuses = ["Delivered", "In Transit", "Processing", "Pending Payment", "Return Requested", "Cancelled", "Delayed"]
        payments = ["VNPay QR – Paid", "MoMo Wallet – Paid", "Cash on Delivery – Pending", "Credit Card (Visa) – Paid", "Techcombank Banking – Paid"]

        start_date = datetime(2025, 1, 1)

        for _ in range(target_orders):
            oid = f"VN{order_counter}"
            order_counter += 1
            if oid in existing_order_ids:
                continue

            user = random.choice(all_users)
            order_status = random.choice(statuses)
            payment_info = random.choice(payments)
            
            random_days = random.randint(0, 150)
            o_date = start_date + timedelta(days=random_days, hours=random.randint(8, 20))
            o_date_str = o_date.strftime("%Y-%m-%d")

            est_deliv_str = (o_date + timedelta(days=random.randint(2, 5))).strftime("%Y-%m-%d") if order_status in ["In Transit", "Processing", "Delayed"] else None
            deliv_date_str = (o_date + timedelta(days=random.randint(1, 4))).strftime("%Y-%m-%d") if order_status == "Delivered" else None

            carrier = random.choice(CARRIERS) if order_status in ["In Transit", "Delivered", "Delayed", "Return Requested"] else None
            tracking_no = f"{carrier[:3].upper()}-{random.randint(10000000, 99999999)}" if carrier else None
            address = f"{random.randint(1, 150)} {random.choice(STREETS)}, {random.choice(CITIES)}"

            order_obj = OrderTable(
                order_id=oid,
                customer=user.name,
                user_id=user.user_id,
                status=order_status,
                payment=payment_info,
                order_date=o_date_str,
                estimated_delivery=est_deliv_str,
                delivered_date=deliv_date_str,
                carrier=carrier,
                tracking_number=tracking_no,
                delivery_address=address
            )

            # Pick 1-3 items for this order
            num_items = random.randint(1, 3)
            chosen_prods = random.sample(all_products, k=num_items)
            items_objs = []
            total_amount = 0
            for prod in chosen_prods:
                qty = random.randint(1, 2)
                item_total = prod.price_vnd * qty
                total_amount += item_total
                items_objs.append(OrderItemTable(order_id=oid, name=prod.name, quantity=qty, price_vnd=prod.price_vnd))

            session.add(order_obj)
            for it in items_objs:
                session.add(it)

            # Generate corresponding Transaction
            txn_status = "Success" if "Paid" in payment_info else ("Pending" if "Pending" in payment_info else "Completed")
            txn_id = f"TXN-{o_date.strftime('%Y%m%d')}-{random.randint(10000, 99999)}"
            txn_obj = TransactionTable(
                transaction_id=txn_id,
                user_id=user.user_id,
                amount_vnd=total_amount,
                payment_method=payment_info.split(" – ")[0],
                status=txn_status,
                timestamp=o_date.strftime("%Y-%m-%d %H:%M:%S"),
                linked_order=oid,
                bank_reference=f"REF-{random.randint(1000000, 9999999)}"
            )
            session.add(txn_obj)
            new_orders_count += 1
            new_txns_count += 1

        session.commit()
        print(f"Added {new_orders_count} orders and {new_txns_count} transactions.")

        # 4. Generate Support Tickets
        ticket_counter = 886
        existing_tickets = session.exec(select(TicketTable)).all()
        existing_tkt_ids = {t.ticket_id for t in existing_tickets}

        staff_names = ["Nguyen Thi Mai", "Tran Van Binh", "Le Hoang Nam", "Pham Thu Huong", "Chatbot System"]
        tkt_statuses = ["Open", "In Progress", "Resolved", "Closed"]

        new_tkts_count = 0
        for _ in range(target_tickets):
            tkt_id = f"TKT-0{ticket_counter}"
            ticket_counter += 1
            if tkt_id in existing_tkt_ids:
                continue

            user = random.choice(all_users)
            issue_text, priority = random.choice(ISSUE_TEMPLATES)
            t_status = random.choice(tkt_statuses)
            staff = random.choice(staff_names) if t_status != "Open" else None
            
            created_dt = start_date + timedelta(days=random.randint(30, 150), hours=random.randint(8, 18))
            created_str = created_dt.strftime("%Y-%m-%d %H:%M:%S")

            tkt_obj = TicketTable(
                ticket_id=tkt_id,
                user_id=user.user_id,
                user_name=user.name,
                issue=issue_text,
                priority=priority,
                status=t_status,
                assigned_to=staff,
                created=created_str,
                created_at=created_dt.isoformat(),
                last_update=created_dt.strftime("%Y-%m-%d"),
                resolution=f"Handled by {staff}. Status updated to {t_status}." if t_status in ["Resolved", "Closed"] else None
            )
            session.add(tkt_obj)
            new_tkts_count += 1

        session.commit()
        print(f"Added {new_tkts_count} support tickets.")

    print("Database flooding complete!")


if __name__ == "__main__":
    generate_flooded_data(target_users=50, target_orders=150, target_tickets=50)
