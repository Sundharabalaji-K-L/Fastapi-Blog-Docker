import jwt
from jwt import InvalidTokenError
from app.config import settings
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

password_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = settings.SECRET_KEY
REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY
ALGORITHM = settings.ALGORITHM
TOKEN_EXPIRE_MINUTES = settings.TOKEN_EXPIRE_MINUTES
REFRESH_EXPIRE_MINUTES = settings.REFRESH_EXPIRE_MINUTES


def create_token(data: dict, expire_delta: int = None) -> str:
    to_encode = data.copy()

    if expire_delta is None:
        expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_delta)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id: str = payload.get('id')

        if id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could Not Validate Credentials')

    except InvalidTokenError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could Not Validate Credentials')

    return user_id


def get_current_user(token: str = Depends(password_bearer)):
    user_id = verify_token(token)
    return user_id


def create_refresh_token(data: dict, expire_delta: int = None):
    to_encode = data.copy()

    if expire_delta is None:
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_EXPIRE_MINUTES)

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_delta)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

