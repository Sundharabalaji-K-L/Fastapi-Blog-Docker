from fastapi import APIRouter, HTTPException, status
from .schemas import RegisterUser, TokenSchema
from .redis_service import write_to_redis
from .services import add_user
from .utils import verify_user
from .oauth2 import create_token, create_refresh_token
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: RegisterUser):
    new_user = await add_user(user)

    if new_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User Already Exists')

    data = {
        'id': str(new_user.id),
        'username': new_user.username,
        'email': new_user.email,
        'password': new_user.password
    }
    write_to_redis(new_user.email, data)
    return {"message": "User Registered Successfully"}


@router.post('/login', status_code=status.HTTP_200_OK, response_model=TokenSchema)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_id = verify_user(form.username, form.password)

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found')

    if user_id is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')

    data = {'id': user_id}
    token = create_token(data)
    refresh_token = create_refresh_token(data)
    return {'access_token': token, 'refresh_token': refresh_token, 'token_type': 'bearer'}
