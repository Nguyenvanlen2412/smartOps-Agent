import httpx
import os
from typing import Optional
from langchain_core.tools import tool


@tool
def search_products_tool(query: Optional[str] = None, category: Optional[str] = None) -> str:
    """Use this tool to search or list products in the TechShop catalog. Call with no arguments (query=None, category=None) to retrieve all available products. Optionally specify 'query' (keyword/name) or 'category' to filter."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        params = {}
        if query:
            params["query"] = query
        if category:
            params["category"] = category

        r = httpx.get(f"{base_url}/products", params=params, timeout=5)
        if r.status_code != 200:
            return "Could not search products at this time."
        products = r.json()
        if not products:
            filter_desc = f" matching '{query or category}'" if (query or category) else ""
            return f"No products found{filter_desc}."

        lines = [f"Found {len(products)} matching product(s):"]
        for p in products:
            lines.append(
                f"- Product ID: {p['product_id']} | Name: {p['name']} | Category: {p['category']} | "
                f"Price: {p['price_vnd']:,} VND | Stock: {p['stock_quantity']} units | Warranty: {p['warranty_months']} months"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error searching products: {str(e)}"


@tool
def get_product_details_tool(product_id: str) -> str:
    """Use this tool to get full specifications, description, and stock details for a specific product ID (e.g., 'PROD-001')."""
    try:
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        r = httpx.get(f"{base_url}/products/{product_id}", timeout=5)
        if r.status_code != 200:
            return f"Product ID '{product_id}' not found."
        p = r.json()
        return (
            f"Product ID: {p['product_id']}\n"
            f"Name: {p['name']}\n"
            f"Category: {p['category']}\n"
            f"Price (VND): {p['price_vnd']:,} VND\n"
            f"Stock Available: {p['stock_quantity']} units\n"
            f"Warranty: {p['warranty_months']} months\n"
            f"Description: {p['description']}"
        )
    except Exception as e:
        return f"Error retrieving product details: {str(e)}"
