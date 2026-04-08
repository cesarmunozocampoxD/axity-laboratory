"""
conversion.py
-------------
Functions that bridge Pydantic schemas and domain entities.

Concepts covered:
- OrderIn  → Order entity   (input to domain)
- Order entity → OrderOut  (domain to output)
"""

from .entities import BandItem, Order
from .schemas import BandItemOut, OrderIn, OrderOut


def order_in_to_entity(order_in: OrderIn) -> Order:
    """
    Convert a validated ``OrderIn`` schema into an ``Order`` domain entity.

    The Pydantic model guarantees that all data is already clean and valid
    before this function is called, so no extra checks are needed here.
    """
    items = [
        BandItem(
            name=item.name,
            unit_price=item.unit_price,
            quantity=item.quantity,
        )
        for item in order_in.items
    ]
    return Order(band=order_in.band, items=items)


def order_to_out(order: Order) -> OrderOut:
    """
    Convert an ``Order`` domain entity into a serializable ``OrderOut`` schema.

    ``subtotal`` for each item is read from the ``BandItem.subtotal`` property
    so the dataclass remains the single source of truth for monetary calculations.
    """
    items_out = [
        BandItemOut(
            name=item.name,
            unit_price=item.unit_price,
            quantity=item.quantity,
            subtotal=item.subtotal,
        )
        for item in order.items
    ]
    return OrderOut(
        band=order.band,
        items=items_out,
        total=order.total,
        item_count=order.item_count,
    )
