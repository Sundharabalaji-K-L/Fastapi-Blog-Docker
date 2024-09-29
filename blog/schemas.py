from pydantic import BaseModel, Field
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)


class PostUpdate(BaseModel):
    title: str
    content: str
    modified_at: datetime = Field(default_factory=datetime.now)


class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    user_id: str
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    message: str
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)


class UpdateComment(BaseModel):
    message: str
    modified_at: datetime = Field(default_factory=datetime.now)


class CommentResponse(BaseModel):
    id: str
    message: str
    created_at: datetime
    modified_at: datetime
    user_id: str
    post_id: str

    class Config:
        from_attributes = True

