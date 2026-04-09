import requests
from arquitectura_hexagonal.domain.entities.order import Order


class HttpNotificationAdapter:
    """Infrastructure adapter: notifies an external HTTP endpoint about an order.

    Satisfies the NotificationService port.
    In production, point `endpoint` to a real notification service.
    In tests, the `requests` module is mocked so no real network call is made.
    """

    def __init__(self, endpoint: str) -> None:
        self._endpoint = endpoint

    def notify(self, order: Order) -> None:
        payload = {
            "order_id": order.id,
            "product": order.product,
            "total": order.total,
            "status": order.status,
        }
        response = requests.post(self._endpoint, json=payload, timeout=5)
        response.raise_for_status()
