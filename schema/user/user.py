from typing import Optional
from schema import BaseModel

class UserSchema(BaseModel):
    id : int
    username : str
    password: str

class UserPublic(BaseModel):
    id:int
    username: str

class UserUpdate(BaseModel):
    usermame:str
    password: str

class PasswordUpdate(UserPublic):
    password:str
