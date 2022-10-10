from typing import Union, Optional

from pydantic import BaseModel, EmailStr, ValidationError, validator
from beanie import Document, PydanticObjectId


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class BaseUser(BaseModel):
    id: Optional[PydanticObjectId]
    username: str
    full_name: str
    email: EmailStr
    disabled: bool = False


class User(Document, BaseUser):
    hashed_password: str


class UserShow(BaseModel):
    username: str
    full_name: str


class UserCreate(BaseUser):
    password: str

    # @validator('password', check_fields=False)
    # def password(cls, v):
    #     assert v.isalnum(), 'must be alphanumeric'
    #     assert len(v) <= 8, 'too short, must be 8 chars'
    #     return v
