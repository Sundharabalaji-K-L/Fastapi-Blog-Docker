from pydantic import BaseModel, EmailStr, model_serializer
from bson import ObjectId
from datetime import datetime


class User(BaseModel):
    id: ObjectId
    username: str
    email: EmailStr
    password: str
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
        return serialized
