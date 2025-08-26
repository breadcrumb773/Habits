import pytest
import requests
from app.models.creature import Creature
from app.models.explorer import Explorer
from app.data.errors import Duplicate

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session", autouse=True)
def explorer():
    return Explorer(
        name = "Test Explorer", 
        country = "Test Country", 
        description = "Test Description"
    )

@pytest.fixture(scope="session", autouse=True)
def creature():
    return Creature(name="Yeti",
             aka="Abominable Snowman",
             country="CN",
             area="Himalayas",
             description="Hirsute Himalayan"
    )

def test_top_level():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert r.json() == {"message": "This is the top page"}

@pytest.fixture
def create_explorer(explorer):
    params = explorer.model_dump()
    r = requests.post(f"{BASE_URL}/explorer", 
                      json=params)
    print(f"{params = }")
    data_explorer = r.json()
    print(f"{data_explorer = }")
    assert r.status_code == 201,r.status_code
    assert r.headers["content-type"].startswith("application/json")
    assert data_explorer["name"] == explorer.name, r.text
    assert data_explorer["country"] == explorer.country, r.text
    assert data_explorer["description"] == explorer.description, r.text
    return data_explorer

@pytest.fixture
def create_creature(creature):
    params = creature.model_dump()
    r = requests.post(f"{BASE_URL}/creature", 
                      json=params)
    print(f"{params = }")
    data_creature = r.json()
    print(f"{data_creature = }")
    assert r.status_code == 201,r.status_code
    assert data_creature["name"] == creature.name, r.text
    assert data_creature["country"] == creature.country, r.text 
    assert data_creature["description"] == creature.description, r.text
    return data_creature

def test_create_explorer_duplicate(create_explorer):     
        response = requests.post(f"{BASE_URL}/explorer", 
                       json=create_explorer)
        data_explorer = response.json()
        assert response.headers["content-type"].startswith("application/json"),response.headers
        assert response.status_code ==409, response.status_code
        assert "detail" in data_explorer, response.text

def test_create_creature_duplicate(create_creature):     
        response = requests.post(f"{BASE_URL}/creature", 
                       json=create_creature)
        data_creature = response.json()
        assert response.headers["content-type"].startswith("application/json"),response.headers
        assert response.status_code == 409, response.status_code
        assert "detail" in data_creature, response.text