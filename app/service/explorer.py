from app.models.explorer import Explorer
import app.data.explorer as data

data.create_table()

def get_all() -> list[Explorer]:
    return data.get_all()

def get_one(name: str) -> Explorer:
    return data.get_one(name)

def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)

def modify(name: str, explorer: Explorer) -> Explorer:
    return data.modify(name, explorer)

def delete(name: str) -> Explorer:
    return data.delete(name)

 