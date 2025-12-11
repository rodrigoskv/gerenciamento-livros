from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import model
import schema
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

@user.post("/{user_id}/books/{book_id}", response_model=schema.Book)
async def associate_book_to_user(user_id : int, book_id:int, session: AsyncSession = Depends(get_db)):
    db_book = await session.scalar(select(model.Book).where(model.Book.id == book_id))
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Livro não encontrado"
        )
    db_user = session.scalar(select(model.User).where(model.User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado"
        )
    db_book.user_id = user_id
    await session.commit()
    await session.refresh(db_book)
    return db_book
    

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



