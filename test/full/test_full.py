import pytest
import requests
import copy
import uuid

from app.models.creature import Creature
from app.models.explorer import Explorer
from app.data.errors import Duplicate


BASE_URL = "http://localhost:8000"

@pytest.fixture()
def explorer():
    uid = uuid.uuid4().hex[:8]
    return Explorer(
        name = f"Test_Explorer_{uid}", 
        country = "Test_Country",
        description = "Test_Description"
    )

@pytest.fixture()
def creature():
    uid = uuid.uuid4().hex[:8]
    return Creature(name=f"Test_Creature_{uid}",
             aka="Abominable Snowman",
             country="CN",
             area="Himalayas",
             description="Hirsute Himalayan"
    )

def test_top_level():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert r.json() == {"message": "This is the top page"}

@pytest.fixture()
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

@pytest.fixture()
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
        assert response.status_code ==409, f"{response.status_code = }, {response.text = }"
        assert "detail" in data_explorer, response.text

def test_create_creature_duplicate(create_creature):     
        response = requests.post(f"{BASE_URL}/creature", 
                       json=create_creature)
        data_creature = response.json()
        assert response.headers["content-type"].startswith("application/json"),response.headers
        assert response.status_code == 409, f"{response.status_code = }, {response.text = }"
        assert "detail" in data_creature, response.text

def test_modify_creature(create_creature):
     name = create_creature["name"]
     changed_creature = copy.deepcopy(create_creature)
     changed_creature["country"] = "Changed country"
     print(f"test_modify_creature:{changed_creature = }")
     response = requests.patch(f"{BASE_URL}/creature/{name}", json=changed_creature)
     data_creature = response.json()
     print(f"{data_creature = }")
     assert response.status_code == 200, f"{response.status_code = }, {response.text = }"
     assert data_creature["name"] == name, data_creature["name"]
     assert data_creature["country"] == "Changed country", data_creature["country"]

def test_modify_explorer(create_explorer):
     name = create_explorer["name"]
     changed_explorer = copy.deepcopy(create_explorer)
     changed_explorer["country"] = "Changed country"
     response = requests.patch(f"{BASE_URL}/explorer/{name}", json=changed_explorer, 
                               headers={"accept": "application/json"})
     data_explorer = response.json()
     assert response.status_code == 200, f"{response.status_code = }, {response.text = }"
     assert data_explorer["name"] == name, data_explorer["name"]
     assert data_explorer["country"] == "Changed country", data_explorer["country"]

def test_delete_explorer(create_explorer):
     name = create_explorer["name"]
     response = requests.delete(f"{BASE_URL}/explorer/{name}")
     data = response.json()
     assert response.status_code == 200, f"{response.status_code = }, {response.text}"
     assert data == name, response.text

def test_delete_creature(create_creature):
     name = create_creature["name"]
     response = requests.delete(f"{BASE_URL}/creature/{name}")
     data = response.json()
     assert response.status_code == 200, f"{response.status_code = }, {response.text}"
     assert data == name, response.text
     
     