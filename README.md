
---

## 📋 Overview

SmartOps Agent is an intelligent customer support assistant built for **TechShop Vietnam**, a consumer electronics retailer. It leverages **Retrieval-Augmented Generation (RAG)** and **LangChain tool-calling agents** to handle real customer inquiries — from checking order statuses and looking up refund policies to creating support tickets and sending email confirmations — all through natural conversation in both **Vietnamese** and **English**.

The agent autonomously decides which tools to invoke based on the user's intent, chains multiple actions together (e.g., look up an order → create a ticket → send confirmation email), and cites source documents when answering policy questions.

---

## ✨ Features

| Capability | Description |
|---|---|
| **📚 RAG Knowledge Base** | Answers policy & FAQ questions by retrieving relevant chunks from company documents using ChromaDB + HuggingFace embeddings |
| **📦 Order Tracking** | Looks up real-time order status, carrier, tracking number, and ETA via mock API |
| **🎫 Ticket Creation** | Creates support tickets with user ID and issue description |
| **📧 Email Notifications** | Sends confirmation emails to customers after actions are completed |
| **💳 Transaction Lookup** | Checks payment/transaction status and details |
| **🧠 Conversation Memory** | Maintains context across multi-turn conversations |
| **🌐 Bilingual Support** | Handles queries in both Vietnamese and English |
| **🔗 Multi-Step Reasoning** | Chains multiple tools in a single conversation turn (e.g., check order → create ticket → send email) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Interface                             │
│                   (Chainlit Chat / CLI)                          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SmartOps Agent Core                           │
│            LangChain AgentExecutor + Gemini Flash               │
│               (with ConversationBufferMemory)                   │
├──────────┬──────────┬──────────┬──────────┬─────────────────────┤
│          │          │          │          │                      │
│  RAG     │  Order   │  Ticket  │  Email   │  Transaction        │
│  Tool    │  Tool    │  Tool    │  Tool    │  Tool               │
│          │          │          │          │                      │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴────┬────────────────┘
     │          │          │          │          │
     ▼          └──────────┴──────────┴──────────┘
┌──────────┐              │
│ ChromaDB │              ▼
│ Vector   │   ┌────────────────────┐
│ Store    │   │  FastAPI Mock API   │
│          │   │  ┌──────────────┐  │
│  (BGE    │   │  │  Mock DB     │  │
│   Large) │   │  │  (In-Memory) │  │
└──────────┘   │  └──────────────┘  │
               └────────────────────┘
```

---

## 📁 Project Structure

```
smartops-agent/
│
├── agent/                          # AI Agent core
│   ├── agent.py                    # SmartOpsAgent class — LangChain AgentExecutor setup
│   ├── prompt.py                   # System prompt & behavioral instructions
│   └── tools/                      # LangChain tool definitions
│       ├── rag_tool.py             # RAG-based policy/FAQ search
│       ├── order_tool.py           # Order status lookup (GET /orders/{id})
│       ├── ticket_tool.py          # Support ticket creation (POST /tickets)
│       ├── email_tool.py           # Email notification sender (POST /emails/notify)
│       └── transaction_tool.py     # Transaction status lookup (GET /transactions/{id})
│
├── rag/                            # RAG query pipeline
│   ├── retriever.py                # ChromaRetriever — similarity search with BGE embeddings
│   └── qa_chain.py                 # QAChainBuilder — retrieval chain with Gemini LLM
│
├── ingestion/                      # Data ingestion pipeline
│   ├── loader.py                   # Load Markdown files via LangChain TextLoader
│   ├── chunker.py                  # Split by Markdown headers + recursive character splitting
│   └── vectorstore.py              # Embed & persist document chunks into ChromaDB
│
├── mock_api/                       # FastAPI mock backend
│   ├── main.py                     # FastAPI app entry point with CORS
│   ├── mock_db.py                  # In-memory database with typed Pydantic models
│   └── routers/
│       ├── orders.py               # GET /orders/{order_id}
│       ├── transactions.py         # GET /transactions/{txn_id}
│       ├── tickets.py              # POST /tickets
│       └── emails.py               # POST /emails/notify
│
├── ui/                             # Chainlit chat interface
│   ├── app.py                      # Chainlit app entry point
│   └── style/
│       └── style.css               # Custom UI styling
│
├── data/                           # RAG source documents
│   ├── techshop_faq.md             # Frequently Asked Questions
│   ├── techshop_refund_policy.md   # Refund & return policy
│   ├── techshop_sample_data.md     # Sample order/transaction data
│   └── customer_support_chat_log.md# Historical chat logs
│
├── tests/                          # Unit & integration tests
│   ├── test_retriever.py           # RAG retrieval quality tests
│   ├── test_tools.py               # Agent tool unit tests
│   └── test_agent.py               # End-to-end agent tests
│
├── notebooks/                      # Experimentation & debugging
├── .env                            # API keys & config (not committed)
├── .gitignore
└── requirements.txt                # Python dependencies
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | Google Gemini 3.1 Flash Lite | Agent reasoning & RAG answer generation |
| **Agent Framework** | LangChain | Tool-calling agent, memory, prompt management |
| **Embeddings** | HuggingFace `BAAI/bge-large-en-v1.5` | Document embedding for semantic search |
| **Vector Store** | ChromaDB | Persistent vector storage & similarity search |
| **Backend API** | FastAPI + Uvicorn | Mock backend simulating real business systems |
| **Data Validation** | Pydantic v2 | Request/response models & typed database |
| **HTTP Client** | httpx | Agent tool → API communication |
| **Chat UI** | Chainlit | Web-based conversational interface |
| **Text Processing** | LangChain Text Splitters | Markdown-aware document chunking |
| **Language** | Python 3.10+ | Core runtime |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed
- A **Google AI API key** (for Gemini)

### 1. Clone the Repository

```bash
git clone https://github.com/Nguyenvanlen2412/smartOps-Agent.git
cd smartOps-Agent
```

### 2. Create a Virtual Environment

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

Create a `.env` file in the project root:

```env
# Google Gemini API Key
GOOGLE_API_KEY=your-google-api-key-here

# Mock API base URL (default for local development)
API_BASE_URL=http://127.0.0.1:8000
```

### 5. Ingest Documents into ChromaDB

Run the ingestion pipeline to load, chunk, and embed the source documents:

```bash
cd ingestion
python vectorstore.py
cd ..
```

This creates a `chroma_db/` directory with the persisted vector store.

### 6. Start the Mock API Server

```bash
uvicorn mock_api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Visit `http://127.0.0.1:8000/docs` for the interactive Swagger documentation.

### 7. Run the Agent

**Option A — CLI mode:**

```bash
python -m agent.agent
```

**Option B — Chainlit UI:**

```bash
chainlit run ui/app.py
```

---

## 💬 Usage

### Example Conversations

**📦 Order Status Inquiry**
```
You: Đơn hàng VN1024 giao đến đâu rồi?

Agent: Order VN1024 is currently In Transit.
       Carrier: Giao Hang Nhanh (GHN)
       Tracking: GHN-88291047
       Estimated Delivery: 2025-05-22
```

**📚 Policy Question (RAG)**
```
You: What is the refund policy for VNPay payments?

Agent: According to our refund policy, VNPay QR payments are refunded
       to your original VNPay account within 5-7 business days...
       [Source: techshop_refund_policy.md]
```

**🎫 Support Ticket + Email (Multi-step)**
```
You: My order VN1027 headphones are defective. Please help.

Agent: [Checks order VN1027 → Finds return already requested]
       [Creates ticket TKT-XXXX for user U00654]
       [Sends confirmation email to Le Ngoc Linh]

       I've created support ticket TKT-XXXX for your defective
       headphones issue. A confirmation email has been sent to
       ngoc.linh@yahoo.com.
```

**💳 Transaction Lookup**
```
You: Check transaction TXN-20250520-01133

Agent: Transaction ID: TXN-20250520-01133
       Customer: Pham Duc Minh
       Status: Pending
       Amount: 28,990,000 VND
       Note: Awaiting bank confirmation webhook
```

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/orders/{order_id}` | Retrieve order details by ID |
| `GET` | `/transactions/{txn_id}` | Retrieve transaction details by ID |
| `POST` | `/tickets` | Create a new support ticket |
| `POST` | `/emails/notify` | Send email notification to a user |

---

## 🧪 Testing

### Run Unit Tests

```bash
pytest tests/ -v
```

### Test Scenarios

| # | Input | Expected Tool | Expected Behavior |
|---|---|---|---|
| 1 | "Đơn hàng VN1024 đang ở đâu?" | `check_order_status` | Returns carrier + ETA from mock DB |
| 2 | "What is your refund policy?" | `search_company_policy_and_db` | Cites refund policy doc, mentions 7-day window |
| 3 | "Can I return opened earbuds?" | `search_company_policy_and_db` | Says no, quotes non-returnable items |
| 4 | "Create a ticket: my screen is cracked" | `create_ticket` | Returns ticket ID (e.g., TKT-0883) |
| 5 | "Send confirmation email to user U00421" | `send_email_notification` | Confirms email sent |
| 6 | "What payment methods do you accept?" | `search_company_policy_and_db` | Lists all payment methods from FAQ |
| 7 | "Check transaction TXN-20250520-01133" | `check_transaction_status` | Returns Pending status |
| 8 | "What's the weather today?" | None | Politely says it's out of scope |

### Manual API Testing

With the mock server running, you can test endpoints directly:

```bash
# Check an order
curl http://127.0.0.1:8000/orders/VN1024

# Check a transaction
curl http://127.0.0.1:8000/transactions/TXN-20250518-00421

# Create a ticket
curl -X POST http://127.0.0.1:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U00421", "issue": "Screen cracked on delivery"}'

# Send an email notification
curl -X POST http://127.0.0.1:8000/emails/notify \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U00421", "subject": "Ticket Created", "message": "Your ticket has been created."}'
```

---

## 📄 Sample Data

The mock database includes pre-populated data for testing:

- **9 Orders** — statuses: In Transit, Delivered, Pending Payment, Return Requested, Cancelled, Processing, Delayed, Partially Refunded, Shipped
- **8 Transactions** — statuses: Success, Pending, Collected by Driver, Refunded, Partially Refunded
- **5 Support Tickets** — priorities: High, Medium, Low; statuses: Open, In Progress, Resolved, Closed
- **9 Users** — with names and email addresses

---

## 🗺️ Roadmap

- [ ] **Chainlit UI integration** — full chat interface with tool badges and source citations
- [ ] **Docker Compose** — containerize FastAPI + ChromaDB for one-command deployment
- [ ] **LangSmith tracing** — full agent trace visibility for debugging
- [ ] **Vietnamese embedding model** — switch to `bge-m3` for improved Vietnamese text retrieval
- [ ] **Ollama support** — swap Gemini for local Llama models for zero-cost inference

---

## 📝 License

This project is for educational and portfolio demonstration purposes.

---

