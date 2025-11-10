from http import HTTPStatus
from fastapi import APIRouter,HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from models.users.user import User
from database import get_db
from schema.user.user import *

user = APIRouter()

@user.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserSchema)
def create_user(user: UserSchema, session: Session=Depends(get_db())):
    db_user = session.scalar(select(User).where(User.username == user.username))

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Usuário já existente")

    db_user = User(username = user.username, password = user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)


@user.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id : int, user : UserUpdate, session: Session=Depends(get_db())):
    db_user=session.scalar(select(User).where(User.id == user_id))
    if not db_user :
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="ID não encontrado")

    db_user.username = user.usermame
    db_user.password = user.password

    session.add(db_user)
    session.commit(db_user)
    session.refresh(db_user)

    return db_user

@user.put()
def update_password():
    ...

@user.delete()
def delete_user():
    ...

@user.post("/login")
def login_for_acess_token(
        form_data : OAuth2PasswordRequestForm = Depends()
):
    ...


