"""
main.py
-------
Entry point. Demonstrates the full flow:

  raw dict  →  OrderIn (Pydantic validation)
            →  Order   (dataclass entity, derived fields)
            →  OrderOut (Pydantic serialization)
"""

from pydantic import ValidationError

from .conversion import order_in_to_entity, order_to_out
from .schemas import OrderIn


def run() -> None:
    # Simulated raw input (could come from an API, CLI, file, etc.)
    raw_orders = [
        {
            "band": "   pink floyd   ",
            "items": [
                {"name": "The Wall (vinyl)", "unit_price": "25.99", "quantity": 2},
                {"name": "T-Shirt", "unit_price": "18.50"},
            ],
        },
        {
            "band": "Metallica",
            "items": [
                {"name": "Black Album (CD)", "unit_price": 12.0, "quantity": 3},
                {"name": "Cap", "unit_price": 20.0},
                {"name": "Concert Ticket", "unit_price": 85.0, "quantity": 2},
            ],
        },
        {
            # intentionally bad: price is negative → ValidationError
            "band": "Nirvana",
            "items": [{"name": "Nevermind", "unit_price": -5.0}],
        },
    ]

    for raw in raw_orders:
        print("-" * 50)
        try:
            # 1. Validate & normalize input
            order_in = OrderIn.model_validate(raw)

            # 2. Convert to domain entity (derived fields calculated here)
            entity = order_in_to_entity(order_in)

            # 3. Serialize to output schema
            out = order_to_out(entity)

            print(f"Band       : {out.band}")
            print(f"Items      : {out.item_count} units")
            print(f"Total      : {out.model_dump()['total']}")
            print("Line items :")
            for item in out.model_dump()["items"]:
                print(
                    f"  {item['name']:<30} x{item['quantity']}  subtotal: {item['subtotal']}"
                )

        except ValidationError as exc:
            print(f"Validation error for band '{raw.get('band', '?')}':")
            for error in exc.errors():
                print(
                    f"  [{'.'.join(str(loc) for loc in error['loc'])}] {error['msg']}"
                )

    print("-" * 50)

    # Demonstrate ordering: sort orders by total (uses dataclass order=True)
    valid_orders = []
    for raw in raw_orders[:2]:
        order_in = OrderIn.model_validate(raw)
        valid_orders.append(order_in_to_entity(order_in))

    print("\nOrders sorted by total (ascending):")
    for o in sorted(valid_orders):
        print(f"  {o.band:<20}  total = ${o.total:.2f}")


if __name__ == "__main__":
    run()
