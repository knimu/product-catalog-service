import pytest
from service import db
from service.models import Product, Category
from tests.factories import ProductFactory

def test_read_product(app):
    with app.app_context():
        product = ProductFactory()
        product.create()
        found = Product.find(product.id)
        assert found is not None
        assert found.name == product.name

def test_update_product(app):
    with app.app_context():
        product = ProductFactory()
        product.create()
        product.description = "updated description"
        product.update()
        assert Product.find(product.id).description == "updated description"

def test_delete_product(app):
    with app.app_context():
        product = ProductFactory()
        product.create()
        assert len(Product.all()) == 1
        product.delete()
        assert len(Product.all()) == 0

def test_list_all_products(app):
    with app.app_context():
        for product in ProductFactory.create_batch(5):
            product.create()
        assert len(Product.all()) == 5

def test_find_by_name(app):
    with app.app_context():
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        expected_name = products[0].name
        found = Product.find_by_name(expected_name)
        assert len(found) >= 1
        assert all(expected_name.lower() in p.name.lower() for p in found)

def test_find_by_category(app):
    with app.app_context():
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        expected_category = products[0].category
        found = Product.find_by_category(expected_category)
        assert len(found) == sum(p.category == expected_category for p in products)

def test_find_by_availability(app):
    with app.app_context():
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        found = Product.find_by_availability(True)
        assert len(found) == sum(p.available is True for p in products)
        assert all(p.available is True for p in found)
