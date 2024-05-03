import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_homepage(client):
    res = client.get("/")
    assert res.json().get("message") == "Welcome to Biblioteca API"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/login",
        data={
            "username": test_user['email'],
            "password": test_user['password']
        }
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
        "email, password, status_code",
        [
            ("wrongemail@gmailcom", "pass123", 403),
            ("test@gmail.com", "wrongpass", 403),
            ("wrongemail@gmailcom", "wrongpass", 403),
            (None, "pass123", 422),
            ("test@gmail.com", None, 422)
        ]
    )
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "login",
        data={
            "username": email,
            "password": password
        }
    )
    assert res.status_code == status_code
