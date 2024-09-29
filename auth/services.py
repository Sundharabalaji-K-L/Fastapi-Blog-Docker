from app.mongodb import database
from .schemas import RegisterUser
from .redis_service import exists_in_redis
from .utils import hash_password
from .models import User


async def add_user(user: RegisterUser):
    if exists_in_redis(user.email):
        return None

    hashed_password = hash_password(user.password)
    new_user = user.model_dump()
    new_user['password'] = hashed_password

    result = await database['users'].insert_one(new_user)

    return User(**new_user, id=result.inserted_id)


