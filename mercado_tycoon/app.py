import os

from flask import Flask
from flask_login import LoginManager

from models import Product, User, db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

STARTER_CATALOG = [
    # name, category, base_cost, base_price, is_perishable, spoilage_rate_per_hour
    ("Arroz 1kg", "abarrotes", 0.80, 1.30, False, 0.0),
    ("Aceite 1L", "abarrotes", 1.60, 2.40, False, 0.0),
    ("Leche 1L", "lacteos", 0.70, 1.10, True, 0.02),
    ("Pan", "panaderia", 0.30, 0.60, True, 0.05),
    ("Manzanas (kg)", "frutas", 0.90, 1.50, True, 0.03),
    ("Refresco 2L", "bebidas", 1.00, 1.80, False, 0.0),
]


def seed_catalog():
    if Product.query.first() is not None:
        return
    for name, category, base_cost, base_price, is_perishable, spoilage_rate in STARTER_CATALOG:
        db.session.add(
            Product(
                name=name,
                category=category,
                base_cost=base_cost,
                base_price=base_price,
                is_perishable=is_perishable,
                spoilage_rate_per_hour=spoilage_rate,
            )
        )
    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "mercado.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.store import store_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(store_bp)

    with app.app_context():
        db.create_all()
        seed_catalog()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
