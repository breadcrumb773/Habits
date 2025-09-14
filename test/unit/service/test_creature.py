import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from models.habit import Habit
from service import habit as code

sample = Habit(
    name = "Test Habit", 
    color="Test Color",
    cadence="Test Cadence",
    created_at="Test Created At",
    owner_id="Test Owner Id",
)

def test_create():
    resp = code.create(sample)
    assert resp == sample

def test_get_exists():
    resp = code.get_one("Test Llm")
    assert resp == sample

def test_get_not_exists():
    resp = code.get_one("not_exists_llm")
    assert resp is None