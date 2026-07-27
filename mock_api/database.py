# mock_api/database.py
import os
from sqlmodel import SQLModel, create_engine, Session

# Set SQLite database file path in mock_api directory
base_dir = os.path.dirname(os.path.abspath(__file__))
sqlite_file_name = "smartops.db"
sqlite_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


def init_db():
    """Create database tables if they do not exist."""
    SQLModel.metadata.create_all(engine)


def get_db():
    """FastAPI Dependency for database sessions."""
    with Session(engine) as session:
        yield session
