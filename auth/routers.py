from fastapi import APIRouter, HTTPException, status, Query
from pydantic import EmailStr
from fastapi_mail.errors import ConnectionErrors
from .schemas import RegisterUser, TokenSchema, ChangePassword
from .redis_service import write_to_redis
from .services import add_user, get_user_details, verify_email, get_user_by_email, update_password
from .utils import verify_user, create_url_safe_token, verify_url_safe_token, verify_password, hash_password
from .oauth2 import create_token, create_refresh_token, get_current_user
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from utils.mail import mail, send_mail

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

    url_token = create_url_safe_token(data['email'])
    email_verification_endpoint = f"http://localhost:8000/auth/email-verify/{url_token}"
    mail_body = {
        'email': data['username'],
        'project_name': 'blog-app',
        'url': email_verification_endpoint
    }
    message = send_mail(recipient=data['email'],
                        subject="Email Verification",
                        body=mail_body)
    try:
        await mail.send_message(message, template_name='verification.html')
    except ConnectionErrors:
        return {'message': 'User registered successfully! could not send mail'}

    return {"message": "User Registered Successfully! please verify email"}


@router.post('/login', status_code=status.HTTP_200_OK, response_model=TokenSchema)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_id = verify_user(form.username, form.password)

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found')

    if user_id is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')

    user = await get_user_details(user_id)

    if user['is_verified'] is not True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Account Not Verified')

    data = {'id': user_id}
    token = create_token(data)
    refresh_token = create_refresh_token(data)
    return {'access_token': token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


@router.get('/email-verify/{token}', status_code=status.HTTP_202_ACCEPTED)
async def user_verification(token: str):
    token_data = verify_url_safe_token(token)

    if not token_data:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Token for email verification is expired")

    result = await verify_email(token_data['email'])

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {token_data['email']} not found")

    return {'message': 'Email Verified', 'status_code': status.HTTP_202_ACCEPTED}


@router.post('/resend-verification', status_code=status.HTTP_201_CREATED)
async def send_verification_mail(email: str = Query(description="email for resending verification")):
    user = await get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user does not exists')

    url_token = create_url_safe_token(email)
    email_verification_endpoint = f"http://localhost:8000/auth/email-verify/{url_token}"
    mail_body = {
        'email': email,
        'project_name': 'Blog-app',
        'url': email_verification_endpoint
    }

    message = send_mail(recipient=email, subject="Email Verification",
                        body=mail_body)

    try:
        await mail.send_message(message, template_name='verification.html')
    except ConnectionErrors:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Something went wrong')

    return {
        "message": "Mail for email verification has been sent, kindly check your inbox",
        "status_code": status.HTTP_201_CREATED
    }


@router.post('/change-password', status_code=status.HTTP_200_OK)
async def change_password(request: ChangePassword, user_id: str = Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    user = await get_user_details(user_id)

    if not verify_password(request.old_password, user['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid old password")

    hashed_new_password = hash_password(request.new_password)

    result = await update_password(user_id, hashed_new_password)

    if result:
        return {'message': 'Password Updated successfully'}

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

