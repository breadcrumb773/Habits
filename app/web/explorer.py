from fastapi import APIRouter, status, Response
from typing import List

from app.models.explorer import Explorer
import app.service.explorer as service 

router = APIRouter(prefix="/explorer", 
                   tags=["Explorer"])

@router.get("", response_model=List[Explorer])
def get_all() -> list[Explorer]:
    return service.get_all()

@router.get("/{name}", response_model=Explorer) 
def get_one(name:str)-> Explorer:
    return service.get_one(name)

@router.post("", response_model=Explorer, 
                status_code=status.HTTP_201_CREATED)
def create(explorer:Explorer, response:Response) -> Explorer:
    created = service.create(explorer)
    response.headers["Location"] = f"/explorers/{created.name}"
    return created

@router.patch("/{name}", response_model=Explorer)
def modify(name:str, explorer: Explorer) -> Explorer:
    return service.modify(name, explorer)

@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str) -> None:
    service.delete(name)

