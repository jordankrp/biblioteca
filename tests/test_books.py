import pytest
from typing import List
from app import schemas

def test_get_all_books(client, test_books):
    res = client.get('/books/')

    def validate(book):
        return schemas.BookResponseWithRatings(**book)
    books_map = map(validate, res.json())
    books_list = list(books_map)

    assert len(res.json()) == len(test_books)
    assert res.status_code == 200


def test_get_one_book(client, test_books):
    res = client.get(f'/books/{test_books[0].id}')
    assert res.status_code == 200

    book = schemas.BookResponseWithRatings(**res.json())
    assert book.Book.id == test_books[0].id
    assert book.Book.author == test_books[0].author
    assert book.Book.year == test_books[0].year
    assert book.Book.summary == test_books[0].summary


def test_get_nonexistent_book(client):
    res = client.get('/books/8888')
    assert res.status_code == 404


def test_create_book_unauthorised(client):
    res = client.post(
        '/books/',
        json={
            "title": "1984",
            "author": "George Orwell",
            "year": "1949"
        }
    )
    assert res.status_code == 401
    assert res.text == '{"detail":"Not authenticated"}'


@pytest.mark.parametrize(
    "title, author, year, summary", [
        ("1984", "George Orwell", 1949, ""),
        ("Brave New World", "Aldous Huxley", 1932, "Set in a futuristic World State, whose citizens are environmentally engineered into an intelligence-based social hierarchy, the novel anticipates huge scientific advancements in reproductive technology, sleep-learning, psychological manipulation and classical conditioning that are combined to make a dystopian society which is challenged by the story's protagonist."),
    ]
)
def test_create_book_authorised(authorised_client, test_user, title, author, year, summary):
    res = authorised_client.post(
        '/books/',
        json={
            "title": title,
            "author": author,
            "year": year,
            "summary": summary
        }
    )
    created_book = schemas.BookResponse(**res.json())
    assert res.status_code == 201
    assert created_book.title == title
    assert created_book.author == author
    assert created_book.year == year
    assert created_book.summary == summary
    assert created_book.owner_id == test_user['id']


def test_delete_book_unauthorised(client, test_books):
    res = client.delete(f'/books/{test_books[0].id}')
    assert res.status_code == 401
    assert res.text == '{"detail":"Not authenticated"}'


def test_delete_book_authorised(authorised_client, test_books):
    res = authorised_client.delete(f'/books/{test_books[0].id}')
    assert res.status_code == 204


def test_delete_nonexistent_book(authorised_client, test_books):
    res = authorised_client.delete('/books/8888')
    assert res.status_code == 404
    assert res.text == '{"detail":"book with id 8888 does not exist"}'


def test_delete_other_user_book(authorised_client, test_books):
    res = authorised_client.delete(f'/books/{test_books[3].id}')
    assert res.status_code == 403
    assert res.text == '{"detail":"Not authorized to perform requested action."}'

def test_update_book(authorised_client, test_books):
    data = {
        "title": "One Hundred Years of Solitude",
        "author": "Gabriel Garcia Marquez",
        "year": 1967,
        "summary": "The multi-generational story of the Buendía family, whose patriarch, José Arcadio Buendía, founded the fictitious town of Macondo."
    }
    res = authorised_client.put(f"/books/{test_books[0].id}", json=data)
    updated_book = schemas.BookCreate(**res.json())
    assert res.status_code == 200
    assert updated_book.title == data['title']
    assert updated_book.author == data['author']
    assert updated_book.year == data['year']
    assert updated_book.summary == data['summary']


def test_update_other_user_book(authorised_client, test_books):
    data = {
        "title": "Norwegian Wood",
        "author": "Haruki Takamuri",
        "year": 1987
    }
    res = authorised_client.put(f"/books/{test_books[3].id}", json=data)
    assert res.status_code == 403


def test_update_book_unauthorised(client, test_books):
    data = {
        "title": "One Hundred Years of Solitude",
        "author": "Gabriel Garcia Marquez",
        "year": 1967,
        "summary": "The multi-generational story of the Buendía family, whose patriarch, José Arcadio Buendía, founded the fictitious town of Macondo."
    }
    res = client.put(f"/books/{test_books[0].id}", json=data)
    assert res.status_code == 401


def test_update_nonexistent_book(authorised_client, test_books):
    data = {
        "title": "One Hundred Years of Solitude",
        "author": "Gabriel Garcia Marquez",
        "year": 1967,
        "summary": "The multi-generational story of the Buendía family, whose patriarch, José Arcadio Buendía, founded the fictitious town of Macondo."
    }
    res = authorised_client.put("/books/9999", json=data)
    assert res.status_code == 404

