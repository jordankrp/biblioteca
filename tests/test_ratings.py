import pytest
from app import models

@pytest.fixture()
def test_rating(test_books, session, test_user):
    new_rating = models.Rating(
        book_id=test_books[0].id,
        user_id=test_user['id'],
        score=10
    )
    session.add(new_rating)
    session.commit()


def test_rate_book(authorised_client, test_books):
    res = authorised_client.post(
        "/rate/",
        json={
            "book_id": test_books[0].id,
            "score": 8
        }
    )
    assert res.status_code == 201


def test_rate_book_again(authorised_client, test_books, test_rating):
    res = authorised_client.post(
        "/rate/",
        json={
            "book_id": test_books[0].id,
            "score": 9
        }
    )
    assert res.status_code == 201


def test_delete_rating(authorised_client, test_books, test_rating):
    res = authorised_client.delete(
        "/rate/",
        json={
            "book_id": test_books[0].id,
        }
    )
    assert res.status_code == 204


def test_delete_nonexistent_rating(authorised_client, test_books):
    res = authorised_client.delete(
        "/rate/",
        json={
            "book_id": test_books[0].id,
        }
    )
    assert res.status_code == 404


def test_rate_nonexistent_book(authorised_client):
    res = authorised_client.delete(
        "/rate/",
        json={
            "book_id": 9999,
        }
    )
    assert res.status_code == 404


def test_rate_book_unauthorised(client, test_books):
    res = client.post(
        "/rate/",
        json={
            "book_id": test_books[0].id,
            "score": 8
        }
    )
    assert res.status_code == 401