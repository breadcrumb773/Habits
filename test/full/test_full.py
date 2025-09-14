import pytest
import requests
import copy
import uuid

from app.models.llm import Llm
from app.data.errors import Duplicate


BASE_URL = "http://localhost:8000"

@pytest.fixture()
def llm():
    uid = uuid.uuid4().hex[:8]
    return Llm(
        name = f"Test_Llm_{uid}", 
        api_key = "Test_Api_Key",
        api_secret = "Test_Api_Secret",
        api_url = "Test_Api_Url",
        description = "Test_Description",
    )

@pytest.fixture()
def llm():
    uid = uuid.uuid4().hex[:8]
    return Llm(name=f"Test_Llm_{uid}",
             api_key="Test_Api_Key",
             api_secret="Test_Api_Secret",
             api_url="Test_Api_Url",
             description="Test_Description",
             
             
    )

def test_top_level():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert r.json() == {"message": "This is the top page"}

@pytest.fixture()
def create_llm(llm):
    params = llm.model_dump()
    r = requests.post(f"{BASE_URL}/llm", 
                      json=params)
    print(f"{params = }")
    data_llm = r.json()
    print(f"{data_llm = }")
    assert r.status_code == 201,r.status_code
    assert data_llm["name"] == llm.name, r.text
    assert data_llm["api_key"] == llm.api_key, r.text 
    assert data_llm["api_url"] == llm.api_url, r.text
    assert data_llm["description"] == llm.description, r.text
    return data_llm

def test_create_llm_duplicate(create_llm):     
            response = requests.post(f"{BASE_URL}/llm", 
                       json=create_llm)
        data_llm = response.json()
        assert response.headers["content-type"].startswith("application/json"),response.headers
        assert response.status_code == 409, f"{response.status_code = }, {response.text = }"
        assert "detail" in data_llm, response.text
        assert "detail" in data_llm, response.text

def test_modify_llm(create_llm):
     name = create_llm["name"]
     changed_llm = copy.deepcopy(create_llm)
     changed_llm["api_key"] = "Changed api_key"
     print(f"test_modify_llm:{changed_llm = }")
     response = requests.patch(f"{BASE_URL}/llm/{name}", json=changed_llm)
     data_llm = response.json()
     print(f"{data_llm = }")
     assert response.status_code == 200, f"{response.status_code = }, {response.text = }"
     assert data_llm["name"] == name, data_llm["name"]
     assert data_llm["api_key"] == "Changed api_key", data_llm["api_key"]

def test_delete_llm(create_llm):
     name = create_llm["name"]
     response = requests.delete(f"{BASE_URL}/llm/{name}")
     data = response.json()
     assert response.status_code == 200, f"{response.status_code = }, {response.text}"
     assert data == name, response.text
     
     