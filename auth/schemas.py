from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
