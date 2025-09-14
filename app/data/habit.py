from app.models.habit import Habit
from app.data.init_db import get_db,load_dev_env
from app.data.errors import DBError, Missing, Duplicate
import sqlite3


def create_table(db_name: str | None = None, test_mode: bool = False):
    print(f"run create_table in messages.py")
    load_dev_env(test_mode)
    with get_db(db_name) as (conn, cursor):
        cursor.execute(
                """create table if not exists habit(
                        name TEXT PRIMARY KEY,
                        color TEXT,
                        cadence TEXT,
                        created_at TEXT,
                        owner_id TEXT)"""
        )
    
def row_to_model(row:tuple) -> Habit:
    name, color, cadence, created_at, owner_id = row
    return Habit(name=name, color=color, cadence=cadence, created_at=created_at, owner_id=owner_id)

def model_to_dict(creature:Habit) -> dict[str:str]:
    return creature.model_dump()

def get_one(name:str) -> Habit:
    if not name: raise ValueError("name is required")
    
    qry = """SELECT * FROM habit WHERE name = :name"""
    params = {"name": name}
    with get_db() as (conn, cursor):
        try:
            cursor.execute(qry, params)
            row = cursor.fetchone()
        except sqlite3.Error as e:
            raise DBError("DBError during SELECT") from e
    if row is None:
        raise Missing(msg=f"habit name {name} not found")
    return row_to_model(row)

def get_all() -> list[Habit]:
    qry = """SELECT * from habit"""
    with get_db() as (conn, cursor):
        try:
            cursor.execute(qry)
        except sqlite3.Error as e:
            raise DBError("DBError during SELECT") from e
        rows = list(cursor.fetchall())
    return [row_to_model(row) for row in rows]

def create(creature: Habit):
    if not creature: raise ValueError("creature is required")
    qry = """INSERT into habit VALUES
                (:name, :color, :cadence, :created_at, :owner_id)"""
    params = model_to_dict(creature)
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
                raise Duplicate(f"habit name {creature.name} already exists") from e
            raise DBError(f"db integrity error: {name or code}") from e
        except sqlite3.Error as e:
            raise DBError("db error during INSERT") from e
    return get_one(name = creature.name)

def modify(name:str, creature:Habit):
    if not name or not creature:
        raise ValueError("name and creature are required")
    qry = """
            update habit
            set color = :color,
            cadence = :cadence,
            name = :name, 
            created_at = :created_at,
            owner_id = :owner_id
            where name = :name_orig                
        """
    params = model_to_dict(creature)
    params['name_orig'] = name
    with get_db() as (conn, cursor):
        try:
            _ = cursor.execute(qry, params)
            if cursor.rowcount ==0:
                raise Missing(msg = f"habit {name} not found")      
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
                raise Duplicate(f"habit name {creature.name} already exists") from e
            raise DBError(f"db integrity error: {name or code}") from e
    return get_one(name)

def delete(name:str) -> bool:
    if not name: raise ValueError("name is required")

    qry = """DELETE from habit where name = :name"""
    params = {"name" : name}
    with get_db() as (conn, cursor):
        try:
            res = cursor.execute(qry, params)
            if cursor.rowcount ==0:
                raise Missing(msg = f"habit {name} not found")      
        except sqlite3.IntegrityError as e:
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                raise sqlite3.ForeignKeyViolation("fk violation") from e
            else:
                raise DBError(f"db integrity error {e.sqlite_errorname}") from e
        except Exception as e:
            raise DBError("DBerror during delete") from e            
    return name


