"""
TDD: Password Validator — Example-Based Tests
-----------------------------------------------
Red  → Write a failing test first
Green → Write the minimum code to pass
Refactor → Clean up without breaking tests
"""

import pytest  # type: ignore
from pruebas_tdd.password_validator import is_valid, validate_password

# ── RED → GREEN: length rule ──────────────────────────────────────────────────


@pytest.mark.unit
class TestPasswordLength:
    def test_password_shorter_than_8_returns_error(self):
        errors = validate_password("Ab1")
        assert "Password must be at least 8 characters" in errors

    def test_password_of_exactly_8_has_no_length_error(self):
        errors = validate_password("Abcdef1!")
        assert "Password must be at least 8 characters" not in errors

    def test_empty_password_returns_length_error(self):
        errors = validate_password("")
        assert "Password must be at least 8 characters" in errors


# ── RED → GREEN: uppercase rule ───────────────────────────────────────────────


@pytest.mark.unit
class TestPasswordUppercase:
    def test_all_lowercase_returns_uppercase_error(self):
        errors = validate_password("abcdefg1")
        assert "Password must contain at least one uppercase letter" in errors

    def test_one_uppercase_no_uppercase_error(self):
        errors = validate_password("Abcdefg1")
        assert "Password must contain at least one uppercase letter" not in errors


# ── RED → GREEN: digit rule ───────────────────────────────────────────────────


@pytest.mark.unit
class TestPasswordDigit:
    def test_no_digit_returns_digit_error(self):
        errors = validate_password("Abcdefgh")
        assert "Password must contain at least one digit" in errors

    def test_one_digit_no_digit_error(self):
        errors = validate_password("Abcdefg1")
        assert "Password must contain at least one digit" not in errors


# ── Multiple errors ───────────────────────────────────────────────────────────


@pytest.mark.unit
def test_returns_all_errors_for_empty_password():
    errors = validate_password("")
    assert len(errors) == 3


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_valid_password_returns_no_errors(valid_password):
    assert validate_password(valid_password) == []


@pytest.mark.unit
def test_password_factory_produces_valid_password(password_factory):
    pwd = password_factory()
    assert is_valid(pwd)


@pytest.mark.unit
def test_password_factory_without_upper_is_invalid(password_factory):
    pwd = password_factory(upper=False)
    assert not is_valid(pwd)


# ── Parametrize ───────────────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.parametrize(
    "password, expected",
    [
        ("SecurePass1", True),
        ("short1A", False),
        ("nouppercase1", False),
        ("NODIGITONLY", False),
        ("ValidPass9", True),
    ],
    ids=["valid", "too_short", "no_upper", "no_digit", "valid_2"],
)
def test_is_valid_parametrized(password, expected):
    assert is_valid(password) == expected


# ── Skip / xfail examples ─────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.skip(reason="special-char rule not implemented yet")
def test_password_must_have_special_char():
    errors = validate_password("ValidPass1")
    assert "Password must contain at least one special character" in errors


@pytest.mark.unit
@pytest.mark.xfail(reason="unicode edge case under investigation")
def test_unicode_password_raises_no_exception():
    errors = validate_password("Ñoño1234")
    assert isinstance(errors, list)
