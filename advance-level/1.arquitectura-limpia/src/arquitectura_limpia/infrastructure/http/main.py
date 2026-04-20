from arquitectura_limpia.application.events.handlers import OrderCreatedHandler
from arquitectura_limpia.application.presenters.order_presenter import OrderPresenter
from arquitectura_limpia.application.use_cases.create_order import CreateOrderUseCase
from arquitectura_limpia.domain.order import OrderCreated
from arquitectura_limpia.infrastructure.event_bus import EventBus
from arquitectura_limpia.infrastructure.fake_uow import FakeUnitOfWork
from fastapi import FastAPI, status
from pydantic import BaseModel, Field


class CreateOrderRequest(BaseModel):
    order_id: int = Field(gt=0)
    product: str = Field(min_length=1, max_length=100)


class CreateOrderResponse(BaseModel):
    order_id: int
    product: str
    status: str


app = FastAPI(title="Arquitectura Limpia API", version="0.1.0")

_event_bus = EventBus()
_event_bus.register(OrderCreated, OrderCreatedHandler())


@app.post(
    "/orders", response_model=CreateOrderResponse, status_code=status.HTTP_201_CREATED
)
def create_order(payload: CreateOrderRequest) -> CreateOrderResponse:
    use_case = CreateOrderUseCase(
        uow=FakeUnitOfWork(),
        event_bus=_event_bus,
        presenter=OrderPresenter(),
    )
    result = use_case.execute(order_id=payload.order_id, product=payload.product)
    return CreateOrderResponse(**result)
