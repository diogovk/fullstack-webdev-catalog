from app import db
from models import Category, Item

soccer_ball_description = """
A football, soccer ball, or association football ball is the ball used in the
sport of association football. The name of the ball varies according to
whether the sport is called "football", "soccer", or "association football".
More: https://en.wikipedia.org/wiki/Ball_(association_football)
"""

soccer_gloves_description = """
Since the 1980s significant advancements have been made in the design of
gloves, which now feature protectors to prevent the fingers bending
backwards, segmentation to allow greater flexibility, and palms made of
materials designed to protect the hand and to enhance a player's grip.
More: https://en.wikipedia.org/wiki/Kit_(association_football)
"""

seed_data = {
        "Soccer": {"Ball": soccer_ball_description, "Gloves":soccer_gloves_description, "Red Card":"The card used for expulsion of a player."},
        "Basketball": {"Ball":"the inflated ball used in the game of basketball", "Sneakers":"", "Hoop":"Where the ball must pass through for scoring points."},
        "Skating": {"Ice Skates":"", "Roller Skates":""},
        "Volleyball": {"Ball":"", "Net":""},
        "Handball": {"Ball":"", "Goal":""},
        "Magic": {"Sleeves":"Used to protect the cards from scratches and dust", "Playmat":""},
        "Swimming": {"Swimming Googles":"Used to see under water", "Swimsuit":""},
        "Tennis": {"Tennis Ball":"", "Racket":"Used to hit the ball"}
        }

for category_name, items in seed_data.items():
    category = Category(name=category_name)
    db.session.add(category)
    db.session.commit()
    for (item_name, description) in items.items():
        item = Item(name=item_name, category_id=category.id, description=description)
        db.session.add(item)
        db.session.commit()
