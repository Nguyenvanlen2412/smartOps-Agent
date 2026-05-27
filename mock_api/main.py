# mock_api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers (Stubs included for tickets, transactions, emails based on your requirements)
from mock_api.routers import emails, tickets, orders, transactions
# from mock_api.routers import tickets, transactions, emails 

app = FastAPI(
    title="TechShop Mock API",
    description="A simplified mock API acting as the backend data system for AI Agent tool calling.",
    version="1.0.0"
)

# Configure CORS to ensure local agents or web frontends can call endpoints smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits requests from any origin; perfect for a local developer sandbox
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

# Register routers
app.include_router(orders.router)
app.include_router(tickets.router)
app.include_router(transactions.router)
app.include_router(emails.router)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the TechShop Mock API",
        "docs": "Navigate to /docs to view the interactive Swagger API documentation."
    }