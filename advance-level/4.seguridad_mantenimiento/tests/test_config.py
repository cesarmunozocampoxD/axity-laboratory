"""
Tests for pydantic-settings configuration and application helpers.

Key security assertions:
- SecretStr values must NOT appear in repr/str output.
- Settings must be overridable via environment variables (12-factor).
- get_app_info must never leak the api_key.
"""

from unittest.mock import MagicMock, patch

from seguridad_mantenimiento.app import get_app_info
from seguridad_mantenimiento.config import Settings

# ---------------------------------------------------------------------------
# Settings: loading and defaults
# ---------------------------------------------------------------------------


def test_default_values_are_applied():
    settings = Settings(_env_file=None)  # skip .env file in tests

    assert settings.app_name == "seguridad-mantenimiento"
    assert settings.debug is False
    assert settings.port == 8000
    assert settings.database_url == "sqlite:///./app.db"


def test_settings_overridden_by_environment_variables():
    overrides = {
        "APP_NAME": "test-app",
        "DEBUG": "true",
        "PORT": "9000",
        "DATABASE_URL": "postgresql://user:pass@localhost/testdb",
    }
    with patch.dict("os.environ", overrides, clear=False):
        settings = Settings(_env_file=None)

    assert settings.app_name == "test-app"
    assert settings.debug is True
    assert settings.port == 9000
    assert "postgresql" in settings.database_url


# ---------------------------------------------------------------------------
# Secret handling
# ---------------------------------------------------------------------------


def test_api_key_secret_not_exposed_in_repr():
    """SecretStr must mask the value; it must not appear in the object repr."""
    with patch.dict("os.environ", {"API_KEY": "ultra-secret-123"}):
        settings = Settings(_env_file=None)

    assert "ultra-secret-123" not in repr(settings)
    assert "ultra-secret-123" not in str(settings)


def test_api_key_is_accessible_explicitly():
    """The real value must still be retrievable via get_secret_value()."""
    with patch.dict("os.environ", {"API_KEY": "ultra-secret-123"}):
        settings = Settings(_env_file=None)

    assert settings.api_key.get_secret_value() == "ultra-secret-123"


# ---------------------------------------------------------------------------
# get_app_info: public surface
# ---------------------------------------------------------------------------


def test_get_app_info_returns_expected_keys():
    mock_settings = MagicMock()
    mock_settings.app_name = "demo-app"
    mock_settings.debug = False
    mock_settings.port = 8080
    mock_settings.database_url = "sqlite:///test.db"

    info = get_app_info(mock_settings)

    assert info == {
        "name": "demo-app",
        "debug": False,
        "port": 8080,
        "database_url": "sqlite:///test.db",
    }


def test_get_app_info_does_not_contain_api_key():
    """app_info is the public surface — the api_key field must not be in it."""
    with patch.dict("os.environ", {"API_KEY": "should-not-appear"}):
        settings = Settings(_env_file=None)
        info = get_app_info(settings)

    assert "api_key" not in info
    assert "should-not-appear" not in str(info)
