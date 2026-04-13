import requests

from .config import API_BASE_URL


def list_orders() -> list[dict]:
    response = requests.get(API_BASE_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    # dummyjson wraps results in a "carts" key
    return data.get("carts", data) if isinstance(data, dict) else data


def create_order(user_id: int, product_id: int, quantity: int) -> dict:
    payload = {
        "userId": user_id,
        "products": [{"id": product_id, "quantity": quantity}],
    }
    response = requests.post(f"{API_BASE_URL}/add", json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def delete_order(order_id: int) -> dict:
    response = requests.delete(f"{API_BASE_URL}/{order_id}", timeout=10)
    response.raise_for_status()
    return response.json()
