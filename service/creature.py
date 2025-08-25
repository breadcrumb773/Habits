from models.creature import Creature
import fake.creature as data


def get_all() -> list[Creature]:
    """Return all creatures"""
    return data.get_all()

def get_one(name: str) -> Creature | None:
    return data.get_one(name)

def create(creature: Creature) -> Creature:
    return data.create(creature)

def modify(name: str, creature: Creature) -> Creature:
    return data.modify(name, creature)

def replace(name: str, creature: Creature) -> Creature:
    """Completely replace a creature"""
    return data.replace(name, creature)

def delete(name: str):
    return data.delete(name)