from arquitectura_limpia.application.events.handlers import OrderCreatedHandler
from arquitectura_limpia.application.presenters.order_presenter import OrderPresenter
from arquitectura_limpia.application.use_cases.create_order import CreateOrderUseCase
from arquitectura_limpia.domain.order import Order, OrderCreated
from arquitectura_limpia.infrastructure.event_bus import EventBus
from arquitectura_limpia.infrastructure.fake_uow import FakeUnitOfWork

# ── Domain tests ──────────────────────────────────────────────────────────────


def test_order_entity_records_created_event():
    """The entity itself records the OrderCreated event on construction."""
    order = Order(order_id=1, product="Laptop")

    assert len(order.events) == 1
    assert isinstance(order.events[0], OrderCreated)
    assert order.events[0].order_id == 1
    assert order.events[0].product == "Laptop"


def test_order_initial_status_is_created():
    order = Order(order_id=2, product="Phone")

    assert order.status == "created"


# ── Presenter tests ───────────────────────────────────────────────────────────


def test_order_presenter_formats_output():
    """Presenter translates the domain entity into a delivery-friendly dict."""
    order = Order(order_id=3, product="Monitor")
    presenter = OrderPresenter()

    result = presenter.present(order)

    assert result == {"order_id": 3, "product": "Monitor", "status": "created"}


# ── Application / use case tests ──────────────────────────────────────────────


def test_create_order_persists_and_commits():
    """Use case saves the order and commits the Unit of Work."""
    uow = FakeUnitOfWork()
    use_case = CreateOrderUseCase(
        uow=uow, event_bus=EventBus(), presenter=OrderPresenter()
    )

    use_case.execute(order_id=10, product="Keyboard")

    assert uow.committed is True
    saved = uow.orders.get_by_id(10)
    assert saved is not None
    assert saved.product == "Keyboard"


def test_create_order_returns_presenter_output():
    """Use case returns the dict produced by the presenter."""
    uow = FakeUnitOfWork()
    use_case = CreateOrderUseCase(
        uow=uow, event_bus=EventBus(), presenter=OrderPresenter()
    )

    result = use_case.execute(order_id=11, product="Tablet")

    assert result == {"order_id": 11, "product": "Tablet", "status": "created"}


def test_create_order_dispatches_order_created_event():
    """After commit, the use case publishes the OrderCreated event."""
    uow = FakeUnitOfWork()
    event_bus = EventBus()
    received: list[OrderCreated] = []

    class SpyHandler:
        def handle(self, event: OrderCreated) -> None:
            received.append(event)

    event_bus.register(OrderCreated, SpyHandler())
    use_case = CreateOrderUseCase(
        uow=uow, event_bus=event_bus, presenter=OrderPresenter()
    )

    use_case.execute(order_id=20, product="Headphones")

    assert len(received) == 1
    assert received[0].order_id == 20
    assert received[0].product == "Headphones"


def test_event_is_dispatched_after_commit():
    """Events must be dispatched AFTER commit, never before."""
    commit_order: list[str] = []

    class TrackingUoW(FakeUnitOfWork):
        def commit(self) -> None:
            commit_order.append("commit")
            super().commit()

    class TrackingHandler:
        def handle(self, event: OrderCreated) -> None:
            commit_order.append("event_dispatched")

    event_bus = EventBus()
    event_bus.register(OrderCreated, TrackingHandler())

    use_case = CreateOrderUseCase(
        uow=TrackingUoW(), event_bus=event_bus, presenter=OrderPresenter()
    )
    use_case.execute(order_id=30, product="Mouse")

    assert commit_order == ["commit", "event_dispatched"]


# ── Event handler test ────────────────────────────────────────────────────────


def test_order_created_handler_prints_confirmation(capsys):
    """The application handler reacts to the OrderCreated event."""
    handler = OrderCreatedHandler()
    event = OrderCreated(order_id=99, product="Webcam")

    handler.handle(event)

    output = capsys.readouterr().out
    assert "99" in output
    assert "Webcam" in output
