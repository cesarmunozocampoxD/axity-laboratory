from datetime import datetime

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    customer_name: str = Field(..., max_length=100)
    product: str = Field(..., max_length=200)
    quantity: int = Field(..., gt=0)
    total_price: float = Field(..., gt=0)


class OrderUpdate(BaseModel):
    customer_name: str | None = Field(default=None, max_length=100)
    product: str | None = Field(default=None, max_length=200)
    quantity: int | None = Field(default=None, gt=0)
    total_price: float | None = Field(default=None, gt=0)


class OrderRead(BaseModel):
    id: int
    customer_name: str
    product: str
    quantity: int
    total_price: float
    created_at: datetime

    model_config = {"from_attributes": True}
