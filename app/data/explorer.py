from app.models.explorer import Explorer
from app.data.init_db import get_db,load_dev_env
from app.data.errors import DBError, Missing, Duplicate
import sqlite3

def create_table(db_name: str | None = None, test_mode: bool = False):
    load_dev_env(test_mode)
    with get_db(db_name) as (conn, cursor):
        cursor.execute(
            """create table if not exists explorer(
                        name TEXT PRIMARY KEY,
                        country TEXT,                        
                        description TEXT)""")
    
def row_to_model(row:tuple) -> Explorer:
    name, country, description = row
    return Explorer(name= name, country=country, description=description)

def model_to_dict(explorer:Explorer) -> dict[str:str]:
    return explorer.model_dump()

def get_one(name:str) -> Explorer:
    if not name: ValueError("name is requred")

    qry = """SELECT * FROM explorer WHERE name = :name"""
    params = {"name": name}
    with get_db() as (conn, cursor):
        try:        
            cursor.execute(qry, params)
            row = cursor.fetchone()
        except sqlite3.Error as e:
            raise DBError("DBError during SELECT") from e
    if row is None:
        raise Missing(msg=f"Explorer name {name} not found")
    return row_to_model(row)        

def get_all() -> list[Explorer]:
    qry = """SELECT * from explorer"""
    with get_db() as (conn, cursor):
        try:
            cursor.execute(qry)
        except sqlite3.Error as e:
            raise DBError("DBError during SELECT") from e
        rows = list(cursor.fetchall())
    return [row_to_model(row) for row in rows]

def create(explorer: Explorer):
    if not explorer: raise ValueError("explorer is requried")
    qry = """INSERT into explorer VALUES
                (:name, :country, :description)"""
    params = model_to_dict(explorer)
    with get_db() as (conn, cursor):
        try:
            cursor.execute(qry,params)
        except sqlite3.IntegrityError as e:
            code = getattr(e, "sqlite_errorcode", None)
            name = getattr(e, "sqlite_errorname", "")
            is_duplicate = (
                code in (
                    getattr(sqlite3, "SQLITE_CONSTRAINT_UNIQUE", -1),
                    getattr(sqlite3, "SQLITE_CONSTRAINT_PRIMARYKEY", -2),
                )
                or name in ("SQLITE_CONSTRAINT_UNIQUE", "SQLITE_CONSTRAINT_PRIMARYKEY")
            )

            if is_duplicate:
                raise Duplicate(f"Explorer name {explorer.name} already exists") from e

            raise DBError(f"db integrity error: {name or code}") from e
        except sqlite3.Error as e:
            raise DBError("db error during INSERT") from e
    return get_one(explorer.name)

def modify(name:str, explorer:Explorer):
    if not name or not explorer:
        raise ValueError("name and explorer are required")
    qry = """
            update explorer
            set country = :country,
            name = :name, 
            description = :description
            where name = :name_orig                
        """
    params = model_to_dict(explorer)
    params['name_orig'] = name
    with get_db() as (conn, cursor):
        try:
            _ = cursor.execute(qry, params)
            if cursor.rowcount ==0:
                raise Missing(msg = f"Explorer {name} not found")      
        except sqlite3.IntegrityError as e:
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise Duplicate(f"Explorer name {explorer.name} already exists") from e
            raise DBError("DB error during update") from e
    return get_one(explorer.name)        

def delete(name :str) -> bool:
    if not name: raise ValueError("name is required")

    qry = """DELETE from explorer where name = :name"""
    params = {"name" : name}
    with get_db() as (conn, cursor):
        try:
            res = cursor.execute(qry, params)
            if cursor.rowcount == 0:
                raise Missing(msg = f"Explorer {name} not found")
        except sqlite3.IntegrityError as e:
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                raise sqlite3.ForeignKeyViolation("Explorer is referenced by other rows")
            raise DBError(f"Integrity error {e.sqlite_errorcode}") from e
        except Exception as e:
            raise DBError("DBerror during delete") from e            
    return row_to_model(res)



