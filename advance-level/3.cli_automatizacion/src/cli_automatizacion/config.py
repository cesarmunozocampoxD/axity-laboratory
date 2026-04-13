import os

# Base URL for the Orders API.
# Override via environment variable: ORDERS_API_URL=https://your-api.com/carts
API_BASE_URL: str = os.getenv("ORDERS_API_URL", "https://dummyjson.com/carts")
