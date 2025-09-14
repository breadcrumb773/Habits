import pytest

from app.models.habit import Habit
import app.data.habit as code
from app.data.errors import Duplicate


@pytest.fixture(scope="session", autouse=True)
def get_test_db():
   code.create_table(test_mode=True)

@pytest.fixture(scope="module")
def sample_habit():
    yield Habit(name="Test Habit",
                   color="Test Color",
                   cadence="Test Cadence",
                   created_at="Test Created At",
                   owner_id="Test Owner Id",
                   )

def test_create( sample_habit):
    assert code.create(sample_habit) == sample_habit

 