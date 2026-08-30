from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import EventLog, Product, Store, StoreInventory, db
from simulation import catchup_store

store_bp = Blueprint("store", __name__, url_prefix="/store")


def get_current_store():
    store = Store.query.filter_by(user_id=current_user.id).first()
    if store is None:
        abort(404)
    return store


def run_catchup(store):
    inventory_items = StoreInventory.query.filter_by(store_id=store.id).all()
    events = catchup_store(store, inventory_items, now=datetime.utcnow())
    for event in events:
        db.session.add(
            EventLog(
                store_id=store.id,
                type=event["type"],
                detail=f"product_id={event['product_id']} units={event['units']} loss_value={event['loss_value']:.2f}",
            )
        )
    db.session.commit()
    return events


@store_bp.route("/")
@login_required
def dashboard():
    store = get_current_store()
    events = run_catchup(store)

    inventory_items = StoreInventory.query.filter_by(store_id=store.id).all()
    catalog = Product.query.all()

    return render_template(
        "dashboard.html",
        store=store,
        user=current_user,
        inventory_items=inventory_items,
        catalog=catalog,
        spoilage_events=[e for e in events if e["type"] == "spoilage"],
    )


@store_bp.route("/buy", methods=["POST"])
@login_required
def buy():
    store = get_current_store()
    product = Product.query.get_or_404(request.form.get("product_id", type=int))
    quantity = request.form.get("quantity", default=1, type=int)

    if quantity is None or quantity <= 0:
        flash("Cantidad inválida.")
        return redirect(url_for("store.dashboard"))

    cost = product.base_cost * quantity
    if current_user.cash < cost:
        flash("No tienes suficiente efectivo para esa compra.")
        return redirect(url_for("store.dashboard"))

    inventory = StoreInventory.query.filter_by(store_id=store.id, product_id=product.id).first()
    if inventory is None:
        inventory = StoreInventory(store_id=store.id, product_id=product.id, quantity=0)
        db.session.add(inventory)

    current_user.cash -= cost
    inventory.quantity += quantity
    db.session.commit()

    flash(f"Compraste {quantity} x {product.name} por ${cost:.2f}.")
    return redirect(url_for("store.dashboard"))


@store_bp.route("/sell", methods=["POST"])
@login_required
def sell():
    store = get_current_store()
    product = Product.query.get_or_404(request.form.get("product_id", type=int))

    inventory = StoreInventory.query.filter_by(store_id=store.id, product_id=product.id).first()

    if inventory is None or inventory.quantity <= 0:
        store.reputation = max(0.0, store.reputation - 3)
        db.session.commit()
        flash(f"Quiebre de stock: no hay {product.name} disponible.")
        return redirect(url_for("store.dashboard"))

    inventory.quantity -= 1
    current_user.cash += product.base_price
    store.reputation = min(100.0, store.reputation + 1)
    db.session.commit()

    flash(f"Vendiste 1 x {product.name} por ${product.base_price:.2f}.")
    return redirect(url_for("store.dashboard"))
