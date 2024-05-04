from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    # This drops all tables, then creates them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):

    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@gmail.com", "password": "pass123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorised_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def test_books(test_user, session):
    books_data = [
        {
            "title": "One Hundred Years of Solitude",
            "author": "Gabriel Garcia Marquez",
            "year": "1967",
            "owner_id": test_user['id']
        },
        {
            "title": "The Trial",
            "author": "Franz Kafka",
            "year": "1925",
            "owner_id": test_user['id']
        },
        {
            "title": "The Stranger",
            "author": "Albert Camus",
            "year": "1942",
            "summary": "The story follows Meursault, an indifferent settler in French Algeria, who, weeks after his mother's funeral, kills an unnamed Arab man in Algiers.",
            "owner_id": test_user['id']
        },
    ]

    def create_book_model(book):
        return models.Book(**book)


    books_map = map(create_book_model, books_data)
    books_list = list(books_map)

    session.add_all(books_list)
    #     [
    #         models.Book(
    #             title="One Hundred Years of Solitude",
    #             author="Gabriel Garcia Marquez",
    #             year="1967",
    #             owner_id = test_user['id']
    #         ),
    #         models.Book(
    #             title="The Trial",
    #             author="Franz Kafka",
    #             year="1925",
    #             owner_id = test_user['id']
    #         ),
    #         models.Book(
    #             title="The Stranger",
    #             author="Albert Camus",
    #             year="1942",
    #             summary="The story follows Meursault, an indifferent settler in French Algeria, who, weeks after his mother's funeral, kills an unnamed Arab man in Algiers.",
    #             owner_id = test_user['id']
    #         ),        
    #     ]
    #)
    session.commit()
    books = session.query(models.Book).all()
    return books
