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

