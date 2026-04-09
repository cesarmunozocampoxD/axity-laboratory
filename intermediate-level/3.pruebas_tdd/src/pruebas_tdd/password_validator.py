MIN_LENGTH = 8


def validate_password(password: str) -> list[str]:
    errors = []

    if len(password) < MIN_LENGTH:
        errors.append("Password must be at least 8 characters")

    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")

    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one digit")

    return errors


def is_valid(password: str) -> bool:
    return len(validate_password(password)) == 0
