import pytest
import requests
from fastapi import status

def test_auth_mistake():
    response = requests.get(
        "http://localhost:8000/who", 
        auth = ("wrong_user", "wrong_password"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    assert response.headers["content-type"].startswith("application/json"), response.header
    assert "detail" in response.json()

def test_auth_success():
    response = requests.get("http://localhost:8000/who", auth=("user", "password"))
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.headers["content-type"].startswith("application/json"), response.header
    assert response.json() == {"username": "user", "password": "password"}