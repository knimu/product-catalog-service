from urllib.parse import quote_plus
from tests.factories import ProductFactory
from service.models import Product

BASE_URL = "/products"

def _create_products(client, count=5):
    created = []
    for p in ProductFactory.create_batch(count):
        response = client.post(BASE_URL, json={
            "name": p.name, "description": p.description, "price": p.price,
            "available": p.available, "category": p.category.name
        })
        assert response.status_code == 201
        created.append(response.get_json())
    return created

def test_read_product(client):
    product = _create_products(client, 1)[0]
    response = client.get(f"{BASE_URL}/{product['id']}")
    assert response.status_code == 200
    assert response.get_json()["id"] == product["id"]

def test_update_product(client):
    product = _create_products(client, 1)[0]
    response = client.put(f"{BASE_URL}/{product['id']}", json={"description": "unknown"})
    assert response.status_code == 200
    assert response.get_json()["description"] == "unknown"

def test_delete_product(client):
    product = _create_products(client, 5)[0]
    response = client.delete(f"{BASE_URL}/{product['id']}")
    assert response.status_code == 204
    assert response.data == b""
    assert client.get(f"{BASE_URL}/{product['id']}").status_code == 404

def test_list_all_products(client):
    products = _create_products(client, 5)
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert len(response.get_json()) == len(products) == 5

def test_list_by_name(client):
    products = _create_products(client, 5)
    target_name = products[0]["name"]
    response = client.get(f"{BASE_URL}?name={quote_plus(target_name)}")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert all(target_name.lower() in p["name"].lower() for p in data)

def test_list_by_category(client):
    products = _create_products(client, 10)
    category = products[0]["category"]
    expected = sum(p["category"] == category for p in products)
    response = client.get(f"{BASE_URL}?category={category}")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == expected
    assert all(p["category"] == category for p in data)

def test_list_by_availability(client):
    products = _create_products(client, 10)
    expected = sum(p["available"] is True for p in products)
    response = client.get(f"{BASE_URL}?available=true")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == expected
    assert all(p["available"] is True for p in data)
