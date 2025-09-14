from app.data.init_db import get_user_db, load_dev_env
from .errors import DBError, Missing, Duplicate
from app.models.user import User

import sqlite3
from types import dict

def create_userdb(userdb_name:str| None=None, test_mode:bool=False):
    load_dev_env(test_mode)
    with get_user_db(userdb_name) as (conn_userdb, cursor_userdb):
        cursor_userdb.execute(
            """create table if not exists userdb(
                name TEXT,
                password_hash TEXT,
                status BOOLEAN)""")
        
def model_to_row(user:User)->dict[str, any]:
    return user.model_dump()   

def row_to_model(row:tuple) -> User:
    name, password_hash, status = row
    d = {"name": name, "password_hash": password_hash, "status": bool(status)}
    return User(**d)

def get_all_users() -> list[User]:
    qry = """SELECT name, password_hash, status FROM userdb"""
    with get_user_db() as (conn_userdb, cursor_userdb):
            try:
                cursor_userdb.execute(qry)                
            except sqlite3.Error as e:
                raise DBError("DBError during select all") from e
            else:
                rows = list(cursor_userdb.fetchall())
    return [row_to_model(row) for row in rows]

def get_one_user(user_name:str) -> User:
    if not user_name: raise ValueError("Name is required")

    params = {"username":user_name}
    qry = """SELECT name, password_hash, status FROM userdb where name = :username"""
    with get_user_db() as (conn_userdb, cursor_userdb):
        try:
            cursor_userdb.execute(qry,params)
        except sqlite3.Error as e:
            raise DBError("DBError during get one") from e
        else:
            row= cursor_userdb.fetchone()
    if row in None:
        raise Missing(msg=f"User {user_name} not found")
    return row_to_model(row)

def create(user:User)-> User:
    if not user: raise ValueError("user is required")
    qry = """INSERT into userdb(user_name, hash, status) VALUES(:user_name, :hash, :status)"""
    params = model_to_row(user)
    with get_user_db() as (conn_userdb, cursor_userdb):
        try:
            cursor_userdb.execute(qry,params)
        except sqlite3.IntegrityError as e:
            code = getattr(e, "sqlite_errorcode", None)
            name = getattr(e, "sqlite_errorname", "")
            is_duplicate = (
                code in (
                    getattr(sqlite3, "SQLITE_CONSTRAINT_UNIQUE", -1),
                    getattr(sqlite3,"SQLITE_CONSTRAINT_PRIMARYKEY", -2))
                or
                name in 
                    ("SQLITE_CONSTRAINT_UNIQUE", "SQLITE_CONSTRAINT_PRIMARYKEY")
            )
            if is_duplicate:
                 raise Duplicate(f"User {user.name} already exists") from e
               
            raise DBError("DBError during create user") from e
        except sqlite3.Error as e:
            raise DBError(f"DBError dureing create") from e
        else:
            return get_one_user(user.user_name)
        
def modify(user_name:str, user:User) -> User:
    qry = """update userdb 
            set password_hash= :password_hash, status= :status
            where name = :orig_name"""
    params = model_to_row(user)
    params["orig_name"] = user_name
    with get_user_db as (conn_userdb, cursor_userdb):
        try:
            cursor_userdb.execute(qry, params)
            if cursor_userdb.rowcount ==0:
                Missing(msg = f"User {user_name} not found")
        except sqlite3.IntegrityError as e:
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise Duplicate(f"User name {user.name} already exists") from e
            raise DBError("DB error during update") from e
    return get_one_user(user.name)

def delete_user(user_name:str) -> bool:
    if not user_name: raise ValueError("name is required")
    qry = """DELETE from userdb where user_name = :user_name"""
    params = {"name":user_name}
    with get_user_db() as (conn_userdb, cursor_userdb):
        try:
            res = cursor_userdb.execute(qry, params)
            if cursor_userdb.rowcount == 0:
                raise Missing(msg = f"User {user_name} not found")
        except sqlite3.IntegrityError as e:
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                raise sqlite3.ForeignKeyViolation("User is referenced by other rows")
            raise DBError(f"Integrity error {e.sqlite_errorcode}") from e
        except Exception as e:
            raise DBError("DBerror during delete") from e            
    return user_name