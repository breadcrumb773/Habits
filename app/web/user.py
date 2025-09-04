from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import app.service.user as user_service
from .errors import unauthed
from app.models.user import User

router = APIRouter(prefix="/user", tags="user")
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")

def current_user(token:str = Depends(oauth2_dep)) -> User:
    if not (user := user_service.get_current_user(token)):
       unauthed()
    return user

@router.get("/me")
def me(user:User = Depends(current_user)):
    return user.user_name

@router.post("/token")
async def create_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()):
    """Get username and password from OAuth form, return access token"""
    if not (user := user_service.auth_user(form_data.username, form_data.password)):
        unauthed()
    access_token = user_service.create_access_token(data={'sub':form_data.username})
    return {"access_token":access_token, "token_type":"bearer"}


