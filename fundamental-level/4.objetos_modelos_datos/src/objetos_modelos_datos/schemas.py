"""
schemas.py
----------
Pydantic models for input validation and output serialization.

Theme: orders for rock band merchandise.

Concepts covered:
- BaseModel for input (OrderIn) and output (OrderOut)
- Field() constraints (gt, ge, min_length)
- @field_validator  – normalize / validate a single field
- @model_validator  – cross-field rule (order must have items)
- @field_serializer – custom serialization format
- model_validate()  – parse from dict
- model_dump() / model_dump_json() – serialize to dict / JSON
"""

from pydantic import (
    BaseModel,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

# ---------------------------------------------------------------------------
# Input schemas  (OrderIn)
# ---------------------------------------------------------------------------


class BandItemIn(BaseModel):
    """Validated input for a single merchandise item."""

    name: str = Field(min_length=1, description="Item name, e.g. 'The Wall (vinyl)'")
    unit_price: float = Field(gt=0, description="Price per unit in USD")
    quantity: int = Field(ge=1, default=1, description="Number of units")


class OrderIn(BaseModel):
    """
    Validated input for a merchandise order.

    Validation rules:
    - band name is normalized to Title Case and stripped of whitespace
    - items list must have at least one element
    """

    band: str = Field(min_length=2, description="Rock band name")
    items: list[BandItemIn] = Field(min_length=1, description="Ordered items")

    @field_validator("band")
    @classmethod
    def normalize_band_name(cls, value: str) -> str:
        """Strip surrounding whitespace and apply Title Case."""
        return value.strip().title()

    @model_validator(mode="after")
    def items_must_not_be_empty(self) -> "OrderIn":
        """Guard against an empty items list (redundant with min_length but explicit)."""
        if not self.items:
            raise ValueError("an order must contain at least one item")
        return self


# ---------------------------------------------------------------------------
# Output schemas  (OrderOut)
# ---------------------------------------------------------------------------


class BandItemOut(BaseModel):
    """Serialized representation of a single merchandise item."""

    name: str
    unit_price: float
    quantity: int
    subtotal: float

    @field_serializer("unit_price", "subtotal")
    def serialize_currency(self, value: float) -> str:
        """Format monetary values as '$XX.XX' strings in the JSON output."""
        return f"${value:.2f}"


class OrderOut(BaseModel):
    """Serialized representation of a complete order."""

    band: str
    items: list[BandItemOut]
    total: float
    item_count: int

    @field_serializer("total")
    def serialize_total(self, value: float) -> str:
        return f"${value:.2f}"
