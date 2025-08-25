from fastapi import APIRouter
from models import Creature
# import fake.creature as service
import service.creature as service

router = APIRouter(prefix="/creature")

@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()

@router.get("/{name}")
def get_one(name:str) -> Creature:
    return service.get_one(name)

# all the remaining endpoints do nothing yet:
@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)

@router.patch("/{name}")
def modify(name: str, creature: Creature) -> Creature:
    return service.modify(name, creature)

@router.put("/{name}")
def replace(name: str, creature: Creature) -> Creature:
    return service.replace(name, creature)

@router.delete("/{name}")
def delete(name: str):
    return service.delete(name)