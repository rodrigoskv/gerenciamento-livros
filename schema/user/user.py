from typing import Optional

from schema import BaseModel

class UserSchema(BaseModel):
    username : str
    password: str

class UserPublic(BaseModel):
    id:int
    username: str

class UserId(UserSchema):
    id:int

class UserUpdate(BaseModel):
    username:Optional[str]
    password: Optional[str]

class PasswordUpdate(BaseModel):
    password: Optional[str] = None

