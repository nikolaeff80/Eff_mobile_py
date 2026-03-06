from passlib.hash import bcrypt
from core.models import User


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str) -> User | None:
    try:
        user = User.objects.get(email=email)
        if user.is_active and verify_password(password, user.password_hash):
            return user
        return None
    except User.DoesNotExist:
        return None
    