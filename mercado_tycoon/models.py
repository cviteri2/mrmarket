from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    cash = db.Column(db.Float, nullable=False, default=200.0)

    stores = db.relationship("Store", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    neighborhood_type = db.Column(db.String(50), nullable=False, default="popular")
    rent_cost = db.Column(db.Float, nullable=False, default=10.0)
    reputation = db.Column(db.Float, nullable=False, default=50.0)
    last_update_ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_sales_count = db.Column(db.Integer, nullable=False, default=0)

    inventory = db.relationship("StoreInventory", backref="store", lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    base_cost = db.Column(db.Float, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    is_perishable = db.Column(db.Boolean, nullable=False, default=False)
    spoilage_rate_per_hour = db.Column(db.Float, nullable=False, default=0.0)


class StoreInventory(db.Model):
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    shelf_space_used = db.Column(db.Integer, nullable=False, default=0)

    product = db.relationship("Product")


class EventLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(50), nullable=False)
    detail = db.Column(db.String(255), nullable=False, default="")
