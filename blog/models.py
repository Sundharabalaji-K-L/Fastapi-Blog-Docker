from pydantic import BaseModel, Field, model_serializer
from bson import ObjectId
from datetime import datetime


class Comment(BaseModel):
    id: ObjectId = Field(alias='_id')
    message: str
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    post_id: ObjectId
    user_id: ObjectId

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda date: date.isoformat()
        }

    @model_serializer
    def serialize(self):
        serialized = self.__dict__.copy()
        serialized['id'] = str(serialized['id'])
        serialized['user_id'] = str(serialized['user_id'])
        serialized['post_id'] = str(serialized['post_id'])
        return serialized


class Post(BaseModel):
    id: ObjectId = Field(alias='_id')
    title: str
    content: str
    user_id: ObjectId
    created_at: datetime
    modified_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda date: date.isoformat()
        }

    @model_serializer
    def serialize(self):
        serialized = self.__dict__.copy()

        serialized['id'] = str(serialized['id'])
        serialized['user_id'] = str(serialized['user_id'])
        return serialized

