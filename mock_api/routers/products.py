# mock_api/routers/products.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, col
from typing import Optional, List
from mock_api.database import get_db
from mock_api.models import ProductTable

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("", summary="Search or list products")
def search_products(
    query: Optional[str] = Query(None, description="Search term for product name or category"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    statement = select(ProductTable)
    if category:
        statement = statement.where(col(ProductTable.category).ilike(f"%{category}%"))
    if query:
        statement = statement.where(
            col(ProductTable.name).ilike(f"%{query}%") | col(ProductTable.description).ilike(f"%{query}%")
        )

    products = db.exec(statement).all()
    return [prod.model_dump() for prod in products]


@router.get("/{product_id}", summary="Get product details")
def get_product(product_id: str, db: Session = Depends(get_db)):
    clean_id = product_id.strip().upper()
    statement = select(ProductTable).where(ProductTable.product_id == clean_id)
    product = db.exec(statement).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product ID '{product_id}' not found."
        )
    return product.model_dump()
