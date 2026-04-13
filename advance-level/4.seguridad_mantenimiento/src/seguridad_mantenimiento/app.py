"""
Simple application entry point.

Reads configuration through pydantic-settings and exposes helpers
used by tests and the container CMD.
"""

from seguridad_mantenimiento.config import Settings, get_settings


def get_app_info(settings: Settings | None = None) -> dict:
    """Return public (non-secret) application information."""
    cfg = settings or get_settings()
    return {
        "name": cfg.app_name,
        "debug": cfg.debug,
        "port": cfg.port,
        "database_url": cfg.database_url,
    }


def main() -> None:
    cfg = get_settings()
    info = get_app_info(cfg)
    print(
        f"[{info['name']}] port={info['port']} debug={info['debug']} db={info['database_url']}"
    )
    # api_key is a SecretStr — access the value explicitly only when needed
    print(f"api_key loaded: {'yes' if cfg.api_key else 'no'}")


if __name__ == "__main__":
    main()
