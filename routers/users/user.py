from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from routers.security import *
from routers.auth import *
from schema.token import *
from schema.user.user import *


user = APIRouter()


@user.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: AsyncSession = Depends(get_db)):
    db_user = await session.scalar(select(User).where(User.username == user.username))
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Usuário já existente")

    db_user = User(username = user.username, password = user.password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    await session.close()

    return db_user


@user.put("/{user_id}", response_model=UserPublic)
async def update_user(user_id: int, user: UserUpdate, session: AsyncSession = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Permissões insuficientes'
        )
    try:
        current_user.username = user.username
        current_user.password = user.password
        await session.commit()
        await session.refresh(current_user)
        await session.close()

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Username já existente"
        )


@user.delete("/{user_id}", response_model=str)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Permissões insuficientes"
        )
    await session.delete(current_user)
    await session.commit()
    await session.close()

    return "Usuário deletado"



