# import datetime
# from datetime import timedelta
# from zoneinfo import ZoneInfo
from http import HTTPStatus

from fastapi import Depends, HTTPException
from pwdlib import PasswordHash
from jwt import encode, decode, DecodeError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.dependency import DependencyProcessor


from database import get_db
from models.users.user import User

SECRET_KEY = 'testando'  # provisorio
ALGORITHM = 'HS256'
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = PasswordHash.recommended()

def get_password_hash(password : str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data:dict):
    to_encode=data.copy()
    # expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
    #     minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    # )
    # to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code = HTTPStatus.UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={'WWW-Authenticate' : 'Bearer'}
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_username = payload.get('sub')

        if not subject_username:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.username == subject_username))

    if not user:
        raise credentials_exception

    return user