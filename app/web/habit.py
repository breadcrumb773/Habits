from fastapi import APIRouter, status, Response
from typing import List

from app.models.habit import Habit
import app.service.habit as service


router = APIRouter(prefix="/habit",tags = ["Habit"])

@router.get("", response_model=List[Habit])
def get_all() -> list[Habit]:
    return service.get_all()

@router.get("/{name}", response_model=Habit)
def get_one(name:str) -> Habit:
    return service.get_one(name)

@router.post("", response_model=Habit, 
                status_code=status.HTTP_201_CREATED)
def create(habit: Habit, response:Response) -> Habit:
    created = service.create(habit)
    response.headers["Location"] = f"/habits/{created.name}"
    return created

@router.patch("/{name}", response_model=Habit)
def modify(name: str, habit: Habit) -> Habit:
    return service.modify(name, habit)

@router.delete("/{name}", status_code=status.HTTP_200_OK)
def delete(name: str) -> None:
    return service.delete(name)
