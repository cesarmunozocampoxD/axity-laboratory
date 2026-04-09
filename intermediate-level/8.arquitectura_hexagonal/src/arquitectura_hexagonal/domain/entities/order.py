import uuid
from dataclasses import dataclass, field


@dataclass
class Order:
    """Domain entity representing a customer order.

    Business invariants:
    - quantity must be greater than zero
    - total must be greater than zero
    """

    product: str
    quantity: int
    total: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if self.total <= 0:
            raise ValueError("Total must be greater than zero")
