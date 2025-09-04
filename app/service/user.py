from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError

import app.data.user as data
from app.models.user import User

data.create_userdb()

ALGORITHM="HS256"
SECRET_KEY="secret-key"

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")


def get_hash(plain:str):
    return pwd_context.hash(plain)

def lookup_user(username:str) -> User|None:
    if not (user := data.get(username)):
        return None
    return user 

def verify_password(plain:str, hash:str) -> bool:
    return pwd_context.verify(plain, hash)

def auth_user(name:str, plain:str) -> User|None:
    if not (user := lookup_user(name)):
        return None
    if not verify_password(plain, user.hash):
        return None
    return user

def create_access_token(data:dict, expires:timedelta|None = None):
    src = data.cop()
    if not expires:
        expires = timedelta(minutes=15)
    src.update({"exp":datetime.now()+expires})
    return jwt.encode(src,SECRET_KEY, algorithm=ALGORITHM)

def get_jwt_username(token:str) -> None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['ALGORITHM'])
        if not (username := payload.get("sub")):
            return None        
    except JWTError:
        return None
    return username
    
def get_current_user(token:str) ->User|None:
    if not (username := get_jwt_username(token)):
        return None
    if not (user := lookup_user(username)):
        return None
    return user

def get_all_users() -> list[User]:
    return data.get_all_users()

def get_one_user(user_name:str) -> User:
    return data.get_one_user(user_name)

def modify(user_name:str, user:User) -> User:
    return data.modify(user_name, user)

def create(user:User) -> User:
    return data.create_user(user)

def delete(user_name:str) -> User:
    return data.delete_user(user_name)