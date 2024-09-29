from passlib.context import CryptContext
from .redis_service import get_from_redis, exists_in_redis

password_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def hash_password(password: str):
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


def verify_user(username: str, password: str):
    if not exists_in_redis(username):
        return None

    data = get_from_redis(username)

    if verify_password(password, data['password']):
        return data['id']

    return False
