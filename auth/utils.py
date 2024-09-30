from passlib.context import CryptContext
from .redis_service import get_from_redis, exists_in_redis
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
url_serializer = URLSafeTimedSerializer(secret_key=settings.SECRET_KEY, salt="email-verification.html")

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


def create_url_safe_token(email: str):
    token = url_serializer.dumps(email)
    return token


def verify_url_safe_token(token: str):
    try:
        email = url_serializer.loads(token, max_age=1800)

    except SignatureExpired:
        return None

    except BadSignature:
        return None

    return {'email': email, 'checked': True}




