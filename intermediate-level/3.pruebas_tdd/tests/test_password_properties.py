"""
Property-Based Tests: Password Validator
------------------------------------------
Uses Hypothesis to verify general invariants instead of specific examples.
"""

import string

import pytest  # type: ignore
from hypothesis import given, settings  # type: ignore
from hypothesis import strategies as st  # type: ignore
from pruebas_tdd.password_validator import MIN_LENGTH, is_valid, validate_password

# ── Length property ───────────────────────────────────────────────────────────


@pytest.mark.property
@given(st.text(max_size=MIN_LENGTH - 1))
def test_password_shorter_than_min_always_has_length_error(password):
    errors = validate_password(password)
    assert "Password must be at least 8 characters" in errors


# ── Uppercase property ────────────────────────────────────────────────────────


@pytest.mark.property
@given(
    st.text(
        alphabet=string.ascii_lowercase + string.digits,
        min_size=MIN_LENGTH,
    )
)
def test_password_with_no_uppercase_always_has_uppercase_error(password):
    errors = validate_password(password)
    assert "Password must contain at least one uppercase letter" in errors


# ── Digit property ────────────────────────────────────────────────────────────


@pytest.mark.property
@given(
    st.text(
        alphabet=string.ascii_letters,
        min_size=MIN_LENGTH,
    )
)
def test_password_with_no_digit_always_has_digit_error(password):
    errors = validate_password(password)
    assert "Password must contain at least one digit" in errors


# ── Valid password invariant ──────────────────────────────────────────────────


@pytest.mark.property
@settings(max_examples=200)
@given(
    upper=st.text(alphabet=string.ascii_uppercase, min_size=1),
    lower=st.text(alphabet=string.ascii_lowercase, min_size=1),
    digits=st.text(alphabet=string.digits, min_size=1),
    extra=st.text(alphabet=string.ascii_letters, min_size=5),
)
def test_password_with_all_requirements_is_always_valid(upper, lower, digits, extra):
    password = upper + lower + digits + extra
    assert is_valid(password)


# ── Return type invariant ─────────────────────────────────────────────────────


@pytest.mark.property
@given(st.text())
def test_validate_always_returns_a_list(password):
    result = validate_password(password)
    assert isinstance(result, list)


# ── Idempotency: calling twice returns same result ────────────────────────────


@pytest.mark.property
@given(st.text())
def test_validate_is_deterministic(password):
    assert validate_password(password) == validate_password(password)
