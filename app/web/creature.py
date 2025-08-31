from fastapi import APIRouter, status, Response
from typing import List

from app.models.creature import Creature
import app.service.creature as service


router = APIRouter(prefix="/creature",tags = ["Creature"])

@router.get("", response_model=List[Creature])
def get_all() -> list[Creature]:
    return service.get_all()

@router.get("/{name}", response_model=Creature)
def get_one(name:str) -> Creature:
    return service.get_one(name)

@router.post("", response_model=Creature, 
                status_code=status.HTTP_201_CREATED)
def create(creature: Creature, response:Response) -> Creature:
    created = service.create(creature)
    response.headers["Location"] = f"/creatures/{created.name}"
    return created

@router.patch("/{name}", response_model=Creature)
def modify(name: str, creature: Creature) -> Creature:
    return service.modify(name, creature)

@router.delete("/{name}", status_code=status.HTTP_200_OK)
def delete(name: str) -> None:
    return service.delete(name)
