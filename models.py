from app import db
from sqlalchemy.orm import relationship


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    items = relationship("Item", backref="category")

    @property
    def serialize(self):
        return {
                "id": self.id,
                "name": self.name,
                "items": [item.serialize for item in self.items]
                }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)

    @classmethod
    def get_or_create(cls, email):
        '''
        Returns the user with a certain e-mail, creating one in the database
        if it doesn't exist.
        '''
        user = db.session.query(cls).filter_by(email=email).first()
        if user:
            return user
        else:
            user = cls(email=email)
            db.session.add(user)
            db.session.commit()
            return user


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(500))
    category_id = db.Column(
            db.Integer, db.ForeignKey('category.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_file = db.Column(db.String(128))

    @property
    def url(self):
        return "/item/%s" % self.id

    @property
    def serialize(self):
        return {
                "name": self.name,
                "id": self.id,
                "description": self.description,
                "image_file": self.image_file
                }

    @property
    def serialize_verbose(self):
        return {
                "name": self.name,
                "id": self.id,
                "description": self.description,
                "image_file": self.image_file,
                "category": self.category.name
                }
