# Loads sample data from seed_data.json into the database
from app import db
from models import Category, Item, User
import json

# Creates a user to "own" the sample items
seed_user = User.get_or_create("seeduser@example.com")

if __name__ == '__main__':
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
                        image_file=item["image_file"],
                        owner_id=seed_user.id)
            db.session.add(item)
            db.session.commit()
