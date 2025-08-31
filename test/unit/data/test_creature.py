import pytest

from app.models.creature import Creature
import app.data.creature as code
from app.data.errors import Duplicate


@pytest.fixture(scope="session", autouse=True)
def get_test_db():
   code.create_table(test_mode=True)

@pytest.fixture(scope="module")
def sample_creature():
    yield Creature(name="Test Creature",
                   country="Test Country",
                   area="Test Area",
                   description="Test Description",
                   aka="Test AKA")

def test_create( sample_creature):
    assert code.create(sample_creature) == sample_creature

# def test_create_duplicate(sample_creature):
#      with pytest.raises(Duplicate):
#         _ = code.creature.create(sample_creature)