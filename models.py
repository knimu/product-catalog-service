from enum import Enum
from service import db

class Category(Enum):
    CLOTHS = "Cloths"
    FOOD = "Food"
    HOUSEHOLD = "Household"
    OTHER = "Other"

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False, default="")
    price = db.Column(db.Float, nullable=False, default=0.0)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(db.Enum(Category), nullable=False, default=Category.OTHER)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data):
        if not isinstance(data, dict):
            raise ValueError("Product data must be a JSON object")
        if "name" in data:
            self.name = str(data["name"])
        if "description" in data:
            self.description = str(data["description"])
        if "price" in data:
            self.price = float(data["price"])
        if "available" in data:
            self.available = bool(data["available"])
        if "category" in data:
            raw = data["category"]
            self.category = raw if isinstance(raw, Category) else Category[str(raw).upper()]
        if not self.name:
            raise ValueError("Product name is required")
        return self

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, product_id):
        return cls.query.get(product_id)

    @classmethod
    def all(cls):
        return cls.query.order_by(cls.id).all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(f"%{name}%")).all()

    @classmethod
    def find_by_category(cls, category):
        if not isinstance(category, Category):
            category = Category[str(category).upper()]
        return cls.query.filter_by(category=category).all()

    @classmethod
    def find_by_availability(cls, available=True):
        return cls.query.filter_by(available=available).all()
