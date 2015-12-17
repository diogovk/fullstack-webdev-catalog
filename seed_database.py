from app import db
from models import Category

for category_name in ["Soccer", "Basketball", "Skating", "Volleyball", "Handball", "Magic",
        "Swimming", "Tennis"]:
    category = Category(name = category_name)
    db.session.add(category)

db.session.commit()
