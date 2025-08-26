import sqlite3
import os 
from pathlib import Path
from contextlib import contextmanager

prj_dir = Path(__file__).resolve().parents[1]

def load_dev_env(test_mode:bool = False):
    print(f"run load_dev_env in init_db.py")
    env_config = ".env.test" if test_mode else ".env.dev"
    app_env = os.getenv("APP_ENV", "development").lower()
    env_file = prj_dir.parents[0] / "config"/ env_config
    print(f"{env_file = }")
    print(f"{env_file.exists() = }")
    if app_env != "production" and env_file.exists():
        try:
            from dotenv import load_dotenv
        except Exception as dotenv_load_error:
            print(f"{dotenv_load_error = }")
            return
        load_dotenv(dotenv_path=env_file,override=False)

def get_db_path(db_name:str|None = None) -> str:
    print(f"run get_db_path in init_db.py")
    if db_name:
        return db_name          
    data_dir = prj_dir.parents[0] / "data_db"
    db_name = "criptid_second.db"
    db_path = str(data_dir / db_name)
    final_path = os.getenv("CRYPTID_SQLITE_DB", db_path)
    print(f"{final_path = }")
    return final_path

@contextmanager
def get_db(db_name:str | None = None):
    print(f"run get_db in init_db.py")
    print(f"{db_name = }")
    print(f"{get_db_path(db_name) = }")
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
    

