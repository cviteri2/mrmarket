"""Deterministic catch-up simulation.

No background loop ever runs. Every time a store is loaded, catchup_store()
closes the gap between store.last_update_ts and `now` with an O(n-inventory)
closed-form calculation instead of ticking second by second.
"""
from datetime import datetime

MAX_CATCHUP_SECONDS = 7 * 24 * 3600


def catchup_store(store, inventory_items, now=None):
    """Resolve everything that happened to `store` since its last visit.

    v0.1 has no employees yet, so the only thing that happens while nobody
    is manually tending the store is perishable spoilage. Returns a list of
    event dicts (also suitable for EventLog rows) describing what changed.
    """
    now = now or datetime.utcnow()
    elapsed_seconds = (now - store.last_update_ts).total_seconds()
    elapsed_seconds = max(0.0, min(elapsed_seconds, MAX_CATCHUP_SECONDS))
    elapsed_hours = elapsed_seconds / 3600.0

    events = []
    if elapsed_hours > 0:
        for item in inventory_items:
            product = item.product
            if not product.is_perishable or item.quantity <= 0:
                continue
            spoiled = item.quantity * product.spoilage_rate_per_hour * elapsed_hours
            spoiled_units = min(item.quantity, int(spoiled))
            if spoiled_units > 0:
                item.quantity -= spoiled_units
                events.append(
                    {
                        "type": "spoilage",
                        "product_id": product.id,
                        "units": spoiled_units,
                        "loss_value": spoiled_units * product.base_cost,
                    }
                )

    store.last_update_ts = now
    return events
