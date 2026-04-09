from fastapi import APIRouter, HTTPException, status

from ..core.security import create_access_token, hash_password, verify_password
from ..schemas.token import Token
from ..schemas.user import UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

# Dummy in-memory user store — replace with a real DB lookup
# Passwords are hashed lazily on first request to avoid import-time side-effects
_DUMMY_USERS_RAW = {
    "admin": "secret",
    "user": "password",
}
_DUMMY_USERS: dict[str, str] = {}


def _get_dummy_users() -> dict[str, str]:
    global _DUMMY_USERS
    if not _DUMMY_USERS:
        _DUMMY_USERS = {
            username: hash_password(pw) for username, pw in _DUMMY_USERS_RAW.items()
        }
    return _DUMMY_USERS


@router.post("/login", response_model=Token)
def login(credentials: UserLogin) -> Token:
    hashed = _get_dummy_users().get(credentials.username)
    if not hashed or not verify_password(credentials.password, hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": credentials.username})
    return Token(access_token=access_token)
