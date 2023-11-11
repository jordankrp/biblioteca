from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    year: int
    rating: Optional[int] = None


my_books = [
    {
        "id": 1,
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "description": "A dystopian reality novel that focuses on the social aspects of the dangers behind technological advancements.",
        "year": 1932,
        "rating": 8,
    },
    {
        "id": 2,
        "title": "100 years of solitude",
        "author": "Gabriel Garcia Marquez",
        "year": 1932,
        "rating": 8,
    },
]


def find_book(id):
    for book in my_books:
        if book["id"] == id:
            return book
        
@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@app.get("/books")
def get_books():
    return {"books": my_books}

@app.post("/books")
def create_books(book: Book):
    book_dict = book.dict()
    book_dict['id'] = randrange(0, 100000)
    my_books.append(book_dict)
    return {"new_book": book_dict}

@app.get("/books/{id}")
def get_book(id: int):
    book = find_book(id)
    print(book)
    return {"book_detail": book}