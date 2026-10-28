import requests
from behave import when
from urllib.parse import urljoin

def _endpoint(context, path="products"):
    base = getattr(context, "base_url", "http://127.0.0.1:5000").rstrip("/") + "/"
    return urljoin(base, path.lstrip("/"))

@when('I read the product named "{name}"')
def step_read_product(context, name):
    response = requests.get(_endpoint(context), params={"name": name}, timeout=5)
    assert response.status_code == 200, response.text
    context.results = response.json()

@when('I update the product named "{old_name}" to "{new_name}"')
def step_update_product(context, old_name, new_name):
    response = requests.get(_endpoint(context), params={"name": old_name}, timeout=5)
    assert response.status_code == 200 and response.json(), "Product not found"
    product = response.json()[0]
    response = requests.put(_endpoint(context, f"products/{product['id']}"), json={"name": new_name}, timeout=5)
    assert response.status_code == 200, response.text
    context.results = [response.json()]

@when('I delete the product named "{name}"')
def step_delete_product(context, name):
    response = requests.get(_endpoint(context), params={"name": name}, timeout=5)
    assert response.status_code == 200 and response.json(), "Product not found"
    product = response.json()[0]
    response = requests.delete(_endpoint(context, f"products/{product['id']}"), timeout=5)
    assert response.status_code == 204, response.text
    context.results = requests.get(_endpoint(context)).json()

@when('I list all products')
def step_list_all(context):
    response = requests.get(_endpoint(context), timeout=5)
    assert response.status_code == 200, response.text
    context.results = response.json()

@when('I search by category "{category}"')
def step_search_category(context, category):
    response = requests.get(_endpoint(context), params={"category": category}, timeout=5)
    assert response.status_code == 200, response.text
    context.results = response.json()

@when('I search for available products')
def step_search_available(context):
    response = requests.get(_endpoint(context), params={"available": "true"}, timeout=5)
    assert response.status_code == 200, response.text
    context.results = response.json()

@when('I search by name "{name}"')
def step_search_name(context, name):
    response = requests.get(_endpoint(context), params={"name": name}, timeout=5)
    assert response.status_code == 200, response.text
    context.results = response.json()
