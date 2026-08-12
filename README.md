# 🤖 SmartOps Agent – AI Customer Support & Operations Assistant

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-green.svg)](https://www.langchain.com/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/Database-SQLModel%20%2B%20SQLite-blueviolet.svg)](https://sqlmodel.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/VectorStore-ChromaDB-orange.svg)](https://www.trychroma.com/)
[![Tests](https://img.shields.io/badge/Tests-47%20Passed-brightgreen.svg)](tests/)

---

## 📋 Overview

**SmartOps Agent** is an intelligent customer support and operations assistant built for **TechShop Vietnam**, a consumer electronics retailer. It leverages **Retrieval-Augmented Generation (RAG)** and **LangChain tool-calling agents** (powered by **Google Gemini 3.5 Flash**) to automate real customer inquiries — from checking order statuses, modifying delivery addresses, and verifying warranty policies to creating support tickets, dispatching confirmation emails, and looking up transaction details — all through natural conversation in both **Vietnamese** and **English**.

The agent autonomously plans and decides which of its **15 specialized tools** to invoke based on user intent, seamlessly chaining multiple operational steps together in a single conversation turn (e.g., *look up order status → verify return policy → generate support ticket → dispatch email notification*).

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **📚 RAG Knowledge Base** | Grounded answer generation using ChromaDB vector search + `BAAI/bge-large-en-v1.5` embeddings with source citations |
| **📦 Order Management (6 Tools)** | Check status, list customer orders, cancel orders, update delivery address, request returns, and create new orders |
| **🛍️ Product & Inventory (2 Tools)** | Search product catalog and query detailed product specifications, stock levels, and warranty information |
| **🎫 Ticket Lifecycle (3 Tools)** | Create support tickets, list user tickets, and update ticket resolution status |
| **👤 Customer CRM (1 Tool)** | Fetch user summary profiles and order/ticket history |
| **📧 Notifications (1 Tool)** | Send personalized email confirmation notices to customers |
| **💳 Financial Verification (1 Tool)** | Look up transaction status, payment methods, amounts, and banking references |
| **🧠 Multi-Turn Memory** | Maintains full conversation history and state retention using LangChain `ConversationBufferMemory` |
| **🌐 Bilingual Support** | Seamlessly handles inquiries in both Vietnamese and English |
| **🔗 Autonomous Chaining** | Multi-step reasoning capability to invoke multiple tools in a single logical workflow |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Interface                             │
│                         (CLI)                                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SmartOps Agent Core                           │
│            LangChain AgentExecutor + Gemini 3.5 Flash           │
│               (with ConversationBufferMemory)                   │
├────────┬────────┬────────┬────────┬────────┬────────┬───────────┤
│  RAG   │ Order  │ Product│ Ticket │  User  │ Email  │Txn Status │
│ Tool   │ Tools  │ Tools  │ Tools  │ Tool   │ Tool   │   Tool    │
│ (1)    │ (6)    │ (2)    │ (3)    │ (1)    │ (1)    │   (1)     │
└───┬────┴───┬────┴───┬────┴───┬────┴───┬────┴───┬────┴────┬──────┘
    │        │        │        │        │        │         │
    ▼        └────────┴────────┴────────┴────────┴─────────┘
┌──────────┐                            │
│ ChromaDB │                            ▼
│ Vector   │              ┌────────────────────────────┐
│ Store    │              │   FastAPI REST Backend     │
│ (BGE-    │              │ ┌────────────────────────┐ │
│ Large)   │              │ │ SQLModel (SQLAlchemy)  │ │
│          │              │ │   + SQLite Database    │ │
└──────────┘              │ └────────────────────────┘ │
                          └────────────────────────────┘
```

---

## 📁 Project Structure

```
smartops-agent/
│
├── agent/                          # AI Agent Core
│   ├── agent.py                    # SmartOpsAgent class — LangChain AgentExecutor & Gemini LLM setup
│   ├── prompt.py                   # System prompt & tool selection instructions
│   └── tools/                      # 15 LangChain Tool definitions
│       ├── rag_tool.py             # Policy & FAQ search via RAG QA chain
│       ├── order_tool.py           # Order status, list, cancel, update address, return, create
│       ├── product_tool.py         # Search products & get detailed specs
│       ├── ticket_tool.py          # Create ticket, list tickets, update ticket status
│       ├── user_tool.py            # User summary profile lookup
│       ├── email_tool.py           # Email notification dispatcher
│       └── transaction_tool.py     # Payment/transaction status lookup
│
├── rag/                            # RAG Pipeline Components
│   ├── retriever.py                # ChromaRetriever — similarity search using BGE-Large embeddings
│   └── qa_chain.py                 # QAChainBuilder — retrieval chain with Gemini LLM & source citation
│
├── ingestion/                      # Data Ingestion Pipeline
│   ├── loader.py                   # Load Markdown files via LangChain TextLoader
│   ├── chunker.py                  # Split by Markdown headers + recursive character splitting
│   └── vectorstore.py              # Embed & persist document chunks into ChromaDB
│
├── mock_api/                       # FastAPI REST Server & Database
│   ├── main.py                     # FastAPI entry point with CORS & router wiring
│   ├── database.py                 # SQLModel SQLite database engine & session dependency
│   ├── models.py                   # SQLModel relational table definitions (Users, Products, Orders, Tickets, Txns)
│   ├── seed.py                     # Initial seed data generator
│   └── routers/
│       ├── orders.py               # Order endpoints (GET, POST, PATCH, cancel, return)
│       ├── products.py             # Product lookup endpoints (search, details)
│       ├── tickets.py              # Support ticket endpoints (POST, GET by user, PATCH)
│       ├── users.py                # Customer profile & summary endpoints
│       ├── transactions.py         # Transaction lookup endpoints
│       └── emails.py               # Email dispatch notification endpoint
│
├── data/                           # RAG Source Knowledge Base
│   ├── techshop_faq.md             # Store FAQ document
│   ├── techshop_refund_policy.md   # Return, refund, and shipping policies
│   ├── techshop_sample_data.md     # Reference catalog data
│   └── customer_support_chat_log.md# Historical support conversations
│
├── tests/                          # Automated Test Suite (47 tests)
│   ├── test_agent.py               # End-to-end agent tool chaining tests
│   ├── test_tools.py               # Unit tests for all 15 tools
│   ├── test_ecom_routers.py        # REST API endpoint unit tests
│   ├── test_mock_api_integration.py# Integration tests against live backend
│   └── test_retriever.py           # RAG retrieval accuracy & MRR evaluation
│
├── notebooks/                      # RAG exploration & agent debugging notebooks
├── .env                            # Environment variables (API keys & configuration)
└── requirements.txt                # Project dependencies
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM Engine** | Google Gemini 3.5 Flash Lite | Agent reasoning, tool decision-making & response generation |
| **Agent Framework** | LangChain (`create_tool_calling_agent`) | Tool binding, system prompt management, memory handling |
| **Dense Embeddings** | HuggingFace `BAAI/bge-large-en-v1.5` | 1024-dimensional semantic document embeddings |
| **Vector Store** | ChromaDB | Local persistent vector store for similarity search |
| **Backend REST API** | FastAPI + Uvicorn | Async REST microservice backend |
| **Database & ORM** | SQLModel (SQLAlchemy + Pydantic v2) | Relational ORM models with SQLite persistent database (`smartops.db`) |
| **HTTP Client** | `httpx` | Asynchronous HTTP client for tool API invocations |
| **Testing** | `pytest` | Suite of 47 unit, integration, and MRR evaluation tests |
| **Runtime** | Python 3.10+ | Core runtime environment |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed
- A **Google Gemini API Key** ([Get your key here](https://aistudio.google.com/))

### 1. Clone the Repository

```bash
git clone https://github.com/Nguyenvanlen2412/smartOps-Agent.git
cd smartOps-Agent
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Google Gemini API Key
GOOGLE_API_KEY=your-google-api-key-here

# FastAPI Backend URL
API_BASE_URL=http://127.0.0.1:8000
```

### 5. Run Document Ingestion (ChromaDB)

Process and embed the knowledge base documents into ChromaDB:

```bash
python -m ingestion.vectorstore
```

### 6. Start the Backend API Server

Start the FastAPI backend (which automatically initializes and seeds the SQLite database `smartops.db` on first run):

```bash
uvicorn mock_api.main:app --reload
```

The API will be running at `http://127.0.0.1:8000`. Access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

### 7. Run the SmartOps Agent CLI

In a separate terminal window:

```bash
python -m agent.agent
```

---

## 💬 Usage Examples

### 📦 Order Tracking & Management
```text
You: Đơn hàng VN1024 của tôi đang ở đâu?

Agent: Đơn hàng VN1024 của bạn hiện đang trong trạng thái "In Transit" (Đang vận chuyển).
       • Đơn vị vận chuyển: Giao Hang Nhanh (GHN)
       • Mã vận đơn: GHN-88291047
       • Dự kiến giao hàng: 2025-05-22
       • Địa chỉ nhận: 45 Hoang Quoc Viet, Cau Giay, Hanoi
```

### 📚 Policy Search (RAG with Citation)
```text
You: What is the refund policy for VNPay payments?

Agent: According to TechShop's policy, refunds for orders paid via VNPay QR are processed 
       back to your original VNPay account within 5-7 business days after the return item 
       passes inspection.
       [Source: techshop_refund_policy.md]
```

### 🎫 Multi-Step Ticket Creation & Confirmation Email (Chained Actions)
```text
You: Tai nghe trong đơn VN1027 của tôi bị hỏng một bên. Hãy hỗ trợ tôi.

Agent: Tôi đã kiểm tra đơn hàng VN1027 (Sony WH-1000XM5) và ghi nhận sản phẩm bị lỗi.
       1. Đã tạo yêu cầu hỗ trợ kỹ thuật: Ticket TKT-8832 (Độ ưu tiên: High).
       2. Đã gửi email xác nhận thông tin tới ngoc.linh@yahoo.com.
       Bộ phận chăm sóc khách hàng sẽ liên hệ với bạn trong vòng 24 giờ làm việc!
```

---

## 🔌 API Endpoints Reference

The FastAPI backend provides full CRUD capabilities powered by SQLModel:

| Category | Method | Endpoint | Description |
|---|---|---|---|
| **Orders** | `GET` | `/orders/{order_id}` | Fetch order details by ID |
| | `GET` | `/orders/user/{user_id}` | List all orders for a specific user |
| | `POST` | `/orders` | Create a new customer order |
| | `POST` | `/orders/{order_id}/cancel` | Cancel an eligible order |
| | `PATCH` | `/orders/{order_id}/address` | Update shipping address |
| | `POST` | `/orders/{order_id}/return` | Initiate an order return request |
| **Products** | `GET` | `/products/search?q={query}` | Search product catalog by key terms |
| | `GET` | `/products/{product_id}` | Get product specs, price, and stock levels |
| **Tickets** | `POST` | `/tickets` | Create a support ticket |
| | `GET` | `/tickets/user/{user_id}` | List all support tickets for a user |
| | `PATCH` | `/tickets/{ticket_id}` | Update ticket status and resolution notes |
| **Users** | `GET` | `/users/{user_id}/summary` | Get user summary profile and metrics |
| **Transactions**| `GET` | `/transactions/{txn_id}` | Verify financial transaction status |
| **Emails** | `POST` | `/emails/notify` | Trigger notification email dispatch |

---

## 🧪 Testing & Quality Assurance

The project features a comprehensive **47-test suite** using `pytest` covering units, API router integration, RAG quality, and agent behavior:

```bash
# Run all tests
python -m pytest tests/ -v
```

### Test Coverage Highlights

- **Retriever MRR & Quality (`test_retriever.py`)**: Tests Mean Reciprocal Rank (MRR) and semantic retrieval accuracy across 12 domain query scenarios (return windows, warranties, accepted payment methods).
- **Tool Unit Tests (`test_tools.py`)**: Validates execution logic, error handling, and parameter parsing for all 15 LangChain tools.
- **Router Integration (`test_ecom_routers.py` & `test_mock_api_integration.py`)**: Verifies FastAPI endpoint responses and SQLModel SQLite database queries.
- **End-to-End Agent Execution (`test_agent.py`)**: Tests multi-step tool chaining, tool wiring registration, and prompt compliance.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
