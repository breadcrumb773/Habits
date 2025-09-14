from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

import app.service.user as service
from .errors import unauthed
from app.models.user import User, UserCreate, UserPublic, UserChangePassword
from app.utils import logger_dev

router = APIRouter(prefix="/auth", tags="authentication")
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")

def current_user(token:str = Depends(oauth2_dep)) -> User:
    if not (user := service.get_current_user(token)):
       unauthed()
    return user



@router.post("/login")
async def create_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()):
    """Get username and password from OAuth form, return access token"""
    if not (user := service.auth_user(form_data.username, form_data.password)):
        unauthed()
    access_token = service.create_access_token(data={'sub':form_data.username})
    return {"access_token":access_token, "token_type":"bearer"}

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: Annotated[UserCreate, Depends(UserCreate.as_form)]) -> UserPublic:
    user = service.create_user(user_create)
    return UserPublic(user_name=user.user_name, status=user.status)

@router.post("/change-password", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def change_password(user_change_password: Annotated[UserChangePassword, 
                        Depends(UserChangePassword.as_form())]) -> UserPublic:
    user = service.change_password(user_change_password)
    return UserPublic(user_name=user.user_name, status=user.status)

