from http import HTTPStatus
from fastapi import APIRouter,HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from models.users.user import User
from database import get_db
from routers.users.security import *
from schema.user.user import *
from schema.user.token import *

user = APIRouter()

@user.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session=Depends(get_db)):
    db_user = session.scalar(select(User).where(User.username == user.username))
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Usuário já existente")

    hashed_password = get_password_hash(user.password)

    db_user = User(username = user.username, password = hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@user.put("/users/{user_id}", response_model=UserPublic)
def update_user(user_id : int, user : UserUpdate, session: Session=Depends(get_db)):
    db_user=session.scalar(select(User).where(User.id == user_id))
    if not db_user :
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="ID não encontrado")

    db_user.username = user.username
    db_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(db_user)

    return db_user

# @user.put()
# def update_password():
#     ...
#
# @user.delete()
# def delete_user():
#     ...

@user.post("/token", response_model=Token)
def login_for_access_token(form_data : OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
   db_user = session.scalar(select(User).where(User.username == form_data.username))
   if not db_user:
       raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Email ou senha incorretos")

   if not verify_password(form_data.password, db_user.password):
       raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Email ou senha incorretos")

   access_token = create_access_token(data={'sub':db_user.username})
   return {'access_token': access_token, 'token_type': 'bearer'}



