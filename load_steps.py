import requests
from behave import given
from urllib.parse import urljoin

@given('the following products')
def step_load_products(context):
    base = getattr(context, "base_url", "http://127.0.0.1:5000")
    endpoint = urljoin(base.rstrip("/") + "/", "products")
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "available": row["available"].strip().lower() in ("true", "yes", "1"),
            "category": row["category"].upper(),
        }
        response = requests.post(endpoint, json=payload, timeout=5)
        assert response.status_code == 201, response.text
