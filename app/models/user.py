from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Annotated
from fastapi import Form
from __future__ import annotations
import re

from .errors import UserNameError

MIN_USERNAME_LEN = 3
MAX_USERNAME_LEN = 12
MIN_PWD_LEN = 6
MAX_PWD_LEN = 128


class User(BaseModel):
    user_name:str
    password_hash:str
    status:bool

class UserPublic(BaseModel):
    user_name:str
    status:bool

class UserCreate(BaseModel):
    user_name:Annotated[str, Field(min_length=MIN_USERNAME_LEN,max_length=MAX_USERNAME_LEN)]
    plain:Annotated[str, Field(min_length=MIN_PWD_LEN, max_length=MAX_PWD_LEN)]

    @field_validator("user_name")
    @classmethod
    def no_space(cls, value:str) ->str:
        try:
            if " " in value:
                raise ValueError
        except Exception as e:
             raise UserNameError("username must not contain spaces")
        else:           
            return value
    
    @field_validator("plain")
    def password_stranght(cls, value:str) ->str:
         if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value):
              raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, one number and one special character")
         return value
        
    @model_validator(mode="after")
    def strong_password(self, ) -> UserCreate:
         if self.user_name.lower() in self.plain.lower():
              raise ValueError("password must not contain the username")

    async def as_form(cls,
                    user_name:Annotated[str,Form(...,min_length=MIN_USERNAME_LEN,max_length=MAX_USERNAME_LEN)],
                    plain:Annotated[str,Form(...,min_length=MIN_PWD_LEN, max_length=MAX_PWD_LEN)]
                    ) -> UserCreate:
        return cls(user_name = user_name, plain = plain)
    
class UserChangePassword(UserCreate):
    new_plain:Annotated[str, Field(min_length=MIN_PWD_LEN, max_length=MAX_PWD_LEN)]

    @field_validator("new_plain")
    def password_stranght(cls, value:str) ->str:
         if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value):
              raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, one number and one special character")
         return value
    
    @model_validator(mode="after")
    def equal_oldnew_passwords(self,) -> UserChangePassword:
         if self.new_plain == self.plain:
              raise ValueError("New and old passwords are the same")
         return self

    async def as_form(cls, 
                      user_name:Annotated[str, Form(...,min_length=MIN_USERNAME_LEN,max_length=MAX_USERNAME_LEN)], 
                      plain:Annotated[str, Form(..., min_length=MIN_PWD_LEN, max_length=MAX_PWD_LEN)], 
                      new_plain:Annotated[str, Form(..., min_length=MIN_PWD_LEN, max_length=MAX_PWD_LEN)]) -> UserChangePassword:
         return cls(user_name = user_name,plain = plain, new_plain = new_plain )

