from bson import ObjectId

from app.mongodb import database
from .schemas import RegisterUser
from .redis_service import exists_in_redis, get_from_redis, write_to_redis
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


async def get_user_details(user_id: str):
    user = await database['users'].find_one({'_id': ObjectId(user_id)})

    return user


async def get_user_by_email(email: str):
    user = await database['users'].find_one({'email': email})
    return user


async def verify_email(email: str):
    print(email)
    user = await get_user_by_email(email)
    print(user)
    if user is None:
        return None

    result = await database['users'].update_one(
        {'_id': ObjectId(user['_id'])},
        {'$set': {'is_verified': True}}
    )
    print(result.modified_count)
    return result.modified_count


async def update_user(user_id: str, values: dict):

    result = await database['users'].update_one(
        {'_id': ObjectId(user_id)},
        {'$set': values}
    )

    return result.modified_count


async def update_password(user_id: str, updated_password: str):
    user = await get_user_details(user_id)
    data = get_from_redis(user['email'])

    result = await update_user(user_id, {'password': updated_password})
    data['password'] = updated_password
    write_to_redis(data['email'], data)

    if result:
        return True

    return False



