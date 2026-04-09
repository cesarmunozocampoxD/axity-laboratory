from unittest.mock import patch

import pytest
from arquitectura_hexagonal.domain.entities.order import Order
from arquitectura_hexagonal.infrastructure.notifications.http_notification_adapter import (
    HttpNotificationAdapter,
)
from requests.exceptions import HTTPError

ENDPOINT = "http://notifications.example.com/orders"


@pytest.fixture()
def adapter():
    return HttpNotificationAdapter(ENDPOINT)


@pytest.fixture()
def order():
    return Order(id="ord-1", product="Laptop", quantity=1, total=999.0)


def test_notify_sends_post_to_configured_endpoint(adapter, order):
    with patch(
        "arquitectura_hexagonal.infrastructure.notifications.http_notification_adapter.requests"
    ) as mock_requests:
        mock_requests.post.return_value.raise_for_status.return_value = None

        adapter.notify(order)

        mock_requests.post.assert_called_once_with(
            ENDPOINT,
            json={
                "order_id": "ord-1",
                "product": "Laptop",
                "total": 999.0,
                "status": "pending",
            },
            timeout=5,
        )


def test_notify_calls_raise_for_status(adapter, order):
    """Ensures the adapter propagates HTTP errors from the remote service."""
    with patch(
        "arquitectura_hexagonal.infrastructure.notifications.http_notification_adapter.requests"
    ) as mock_requests:
        mock_requests.post.return_value.raise_for_status.side_effect = HTTPError(
            "500 Server Error"
        )

        with pytest.raises(HTTPError):
            adapter.notify(order)


def test_notify_includes_all_required_fields(adapter, order):
    """Contract: the payload must include order_id, product, total, and status."""
    with patch(
        "arquitectura_hexagonal.infrastructure.notifications.http_notification_adapter.requests"
    ) as mock_requests:
        mock_requests.post.return_value.raise_for_status.return_value = None

        adapter.notify(order)

        _, kwargs = mock_requests.post.call_args
        payload = kwargs["json"]
        assert "order_id" in payload
        assert "product" in payload
        assert "total" in payload
        assert "status" in payload
