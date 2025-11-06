from typing import Optional
from schema import BaseModel

class UserSchema(BaseModel):
    id : int
    username : str
    password: str

class UserPublic(BaseModel):
    username: str
    password : str
