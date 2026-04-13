from arquitectura_limpia.domain.order import OrderCreated

# ── Application-level event handler ──────────────────────────────────────────
# Reacts to the OrderCreated business fact.
# This handler lives in the APPLICATION layer — it may later trigger emails,
# notifications, or other application-level side effects.
# The domain entity knows nothing about this handler.


class OrderCreatedHandler:
    def handle(self, event: OrderCreated) -> None:
        # In a real system this could send an email, push a notification, etc.
        print(
            f"[OrderCreatedHandler] New order confirmed — id: {event.order_id}, product: {event.product}"
        )
