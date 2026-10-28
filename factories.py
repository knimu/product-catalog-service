import factory
from faker import Faker
from service.models import Product, Category

fake = Faker()

class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.LazyFunction(lambda: fake.unique.word().title())
    description = factory.LazyFunction(fake.sentence)
    price = factory.LazyFunction(lambda: round(fake.pyfloat(min_value=1, max_value=500, right_digits=2), 2))
    available = factory.LazyFunction(fake.pybool)
    category = factory.LazyFunction(lambda: fake.random_element(elements=list(Category)))
