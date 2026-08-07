# mock_api/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from mock_api.database import init_db, engine
from mock_api.seed import seed_initial_data
from mock_api.routers import emails, tickets, orders, transactions, products, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed initial data on startup
    init_db()
    with Session(engine) as session:
        seed_initial_data(session)
    yield


app = FastAPI(
    title="TechShop Backend API",
    description="Backend data system & tool API for SmartOps AI Agent with SQLite database persistence.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS to ensure local agents or web frontends can call endpoints smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(orders.router)
app.include_router(tickets.router)
app.include_router(transactions.router)
app.include_router(emails.router)
app.include_router(products.router)
app.include_router(users.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the TechShop Backend API",
        "docs": "Navigate to /docs to view the interactive Swagger API documentation."
    }