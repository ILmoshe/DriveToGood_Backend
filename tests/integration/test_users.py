from fastapi.testclient import TestClient

from app.core.server.app import app
from app.core.routes.user import pwd_context

client = TestClient(app)

CREATE_USER = {"username": "tests", "full_name": "create user",
               "email": "testuser@gmail.com", "password": "test201"}

RESPONSE_USER = {"username": "tests", "fullname": "create user",
                 "email": "testuser@gmail.com", "hashed_password": pwd_context.hash("test201")}


def test_create_user():
    response = client.post("user/sign-up", json=CREATE_USER)
    assert response.status_code == 201
    assert response.json() == RESPONSE_USER
