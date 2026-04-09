import pytest  # type: ignore


@pytest.fixture
def valid_password():
    return "SecurePass1"


@pytest.fixture
def password_factory():
    def make(length=10, upper=True, digit=True):
        pwd = "a" * length
        if upper:
            pwd = "A" + pwd[1:]
        if digit:
            pwd = pwd[:-1] + "1"
        return pwd

    return make
