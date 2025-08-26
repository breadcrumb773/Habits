from app.models.creature import Creature
import app.data.creature as data
from app.data.errors import Missing

data.create_table()
def get_all() -> list[Creature]:
    """Return all creatures"""
    return data.get_all()

def get_one(name: str) -> Creature:
    return data.get_one(name)

def create(creature: Creature) -> Creature:
    return data.create(creature)

def modify(name: str, creature: Creature) -> Creature:
    return data.modify(name, creature)

def delete(name: str) -> Creature:
    return data.delete(name)