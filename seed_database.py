from app import db
from models import Category, Item

seed_data={
        "Soccer": ["Ball", "Gloves", "Red Card"],
        "Basketball": ["Ball", "Sneakers", "Hoop"],
        "Skating": ["Ice Skates", "Roller Skates"],
        "Volleyball": ["Ball", "Net"],
        "Handball": ["Ball", "Goal"],
        "Magic": ["Sleeves", "Playmat"],
        "Swimming": ["Swimming Googles", "Swimsuit"],
        "Tennis": ["Tennis Ball", "Racket"]
        }

for category_name, items in seed_data.items():
    category = Category(name = category_name)
    db.session.add(category)
    db.session.commit()
    for item_name in items:
        item = Item(name = item_name, category_id = category.id)
        db.session.add(item)
        db.session.commit()


