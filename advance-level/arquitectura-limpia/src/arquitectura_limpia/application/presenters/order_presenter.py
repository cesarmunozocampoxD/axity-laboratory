from arquitectura_limpia.domain.order import Order

# ── Presenter ─────────────────────────────────────────────────────────────────
# Translates the domain Order entity into a delivery-friendly dict.
# Lives in the application layer — shapes output without owning business rules.


class OrderPresenter:
    def present(self, order: Order) -> dict:
        return {
            "order_id": order.order_id,
            "product": order.product,
            "status": order.status,
        }
