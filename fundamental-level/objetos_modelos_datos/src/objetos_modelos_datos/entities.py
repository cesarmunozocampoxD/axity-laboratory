"""
entities.py
-----------
Domain entities using dataclasses.

Theme: orders for rock band merchandise (albums, t-shirts, concert tickets).

Concepts covered:
- @dataclass with derived fields via __post_init__
- field() with init=False, repr=False, compare=False
- order=True with sort_index pattern for custom comparisons
- @property for computed attributes
"""

from dataclasses import dataclass, field


@dataclass
class BandItem:
    """A single merchandise item associated with a rock band."""

    name: str
    unit_price: float
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        """Derived: price × quantity."""
        return round(self.unit_price * self.quantity, 2)


@dataclass(order=True)
class Order:
    """
    A merchandise order for a rock band.

    Ordering and equality comparisons are based exclusively on `total`,
    implemented via the `sort_index` pattern:
    - `sort_index` is the only field with compare=True
    - It is set in __post_init__ to mirror `total`
    - All other fields carry compare=False

    Derived fields (set automatically in __post_init__):
    - `total`      : sum of all item subtotals
    - `item_count` : total units across all items
    - `sort_index` : mirrors `total`, used for ordering
    """

    # --- fields excluded from comparisons ---
    band: str = field(compare=False)
    items: list[BandItem] = field(default_factory=list, compare=False)

    # --- derived fields (set in __post_init__) ---
    total: float = field(init=False, compare=False)
    item_count: int = field(init=False, compare=False)

    # --- the sole field used for ordering / equality ---
    sort_index: float = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.total = round(
            sum(item.unit_price * item.quantity for item in self.items), 2
        )
        self.item_count = sum(item.quantity for item in self.items)
        self.sort_index = self.total
