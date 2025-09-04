import sqlite3
import os 
from pathlib import Path
from contextlib import contextmanager

prj_dir = Path(__file__).resolve().parents[1]
data_dir = prj_dir.parents[0] / "data_db"

def load_dev_env(test_mode:bool = False):
    env_config = ".env.test" if test_mode else ".env.dev"
    app_env = os.getenv("APP_ENV", "development").lower()
    env_file = prj_dir.parents[0] / "config"/ env_config
    if app_env != "production" and env_file.exists():
        try:
            from dotenv import load_dotenv
        except Exception as dotenv_load_error:
            print(f"{dotenv_load_error = }")
            return
        load_dotenv(dotenv_path=env_file,override=False)

def get_db_path(db_name:str|None = None) -> str:
    if db_name:
        return db_name  
    db_name = "criptid_second.db"
    db_path = str(data_dir / db_name)
    final_path = os.getenv("CRYPTID_SQLITE_DB", db_path)
    return final_path

@contextmanager
def get_db(db_name:str | None = None):
    conn = sqlite3.connect(get_db_path(db_name), check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    try:
        yield conn, cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_userdb_path(userdb_name:str|None = None)->str:
    if userdb_name:
        return userdb_name
    userdb_name = "second_userdb"
    userdb_path = str(data_dir/userdb_name)
    final_path = os.getenv("USERDB", userdb_path)
    return final_path
    
@contextmanager
def get_user_db(userdb_name:str| None = None) :
    conn_userdb = sqlite3.connect(get_userdb_path(userdb_name), check_same_thread=False)
    conn_userdb.execute("PRAGMA foreign_keys = ON")
    cursor_userdb=conn_userdb.cursor()
    try:
        yield conn_userdb, cursor_userdb
        conn_userdb.commit()
    except Exception:
        conn_userdb.rollback()
        raise
    finally:
        conn_userdb.close()

    
    

