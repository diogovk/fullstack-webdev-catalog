from app import db
from models import Category, Item
import json


if __name__ == '__main__':
    # Load sample data from json file
    with open('seed_data.json') as json_file:
        json_data = json.load(json_file)
    categories_data = json_data["categories"]
    # Add each category and its items in the database
    for category_data in categories_data:
        category = Category(name=category_data["name"])
        db.session.add(category)
        db.session.commit()
        for item in category_data["items"]:
            item = Item(name=item["name"], category_id=category.id,
                        description=item["description"],
                        image_file=item["image_file"])
            db.session.add(item)
            db.session.commit()
