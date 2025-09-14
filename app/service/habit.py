from app.models.habit import Habit
import app.data.habit as data
from app.data.errors import Missing

data.create_table()
def get_all() -> list[Habit]:
    """Return all habits"""
    return data.get_all()

def get_one(name: str) -> Habit:
    return data.get_one(name)

def create(habit: Habit) -> Habit:
    return data.create(habit)

def modify(name: str, habit: Habit) -> Habit:
    return data.modify(name, habit)

def delete(name: str) -> Habit:
    return data.delete(name)