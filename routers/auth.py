from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from routers.security import *
from schema.token import *
from schema.user.user import *


auth = APIRouter()

@auth.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    db_user = session.scalar(select(User).where(User.username == form_data.username))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Email ou senha incorretos")

    if not (form_data.password == db_user.password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Email ou senha incorretos")

    access_token = create_access_token(data={'sub': db_user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}