# ── Event Bus ─────────────────────────────────────────────────────────────────
# Simple in-process event dispatcher.
# Handlers are registered per event type and called synchronously on publish.
# Lives in infrastructure because it is a technical coordination mechanism —
# the application layer only depends on the publish interface.


class EventBus:
    def __init__(self) -> None:
        self.handlers: dict[type, list] = {}

    def register(self, event_type: type, handler) -> None:
        self.handlers.setdefault(event_type, []).append(handler)

    def publish(self, event) -> None:
        for handler in self.handlers.get(type(event), []):
            handler.handle(event)
