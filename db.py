from flask_sqlalchemy import SQLAlchemy

stores = {}
items = {}

db = SQLAlchemy()

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    