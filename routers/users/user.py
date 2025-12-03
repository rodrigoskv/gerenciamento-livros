from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from routers.security import *
from routers.auth import *
from schema.token import *
from schema.user.user import *


user = APIRouter()


@user.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_db)):
    db_user = session.scalar(select(User).where(User.username == user.username))
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Usuário já existente")

    db_user = User(username = user.username, password = user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    session.close()

    return db_user


@user.put("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Permissões insuficientes'
        )
    try:
        current_user.username = user.username
        current_user.password = user.password
        session.commit()
        session.refresh(current_user)
        session.close()

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Username já existente"
        )


@user.delete("/{user_id}", response_model=str)
def delete_user(user_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Permissões insuficientes"
        )
    session.delete(current_user)
    session.commit()
    session.close()

    return "Usuário deletado"



