from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
