import os
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

# Load password from env variables
PASSWORD = os.environ['POSTGRES_PASSWORD']

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    summary: Optional[str] = None
    year: int
    rating: Optional[int] = None
    read: bool = False


try:
    conn = psycopg2.connect(
        host="localhost",
        database="bibliotecadb",
        user="postgres",
        password=PASSWORD,
        cursor_factory=RealDictCursor
    )
    print("Database connection successfull")
except Exception as error:
    print("Connection to DB failed")
    print(f"Error: {error}")

my_books = [
    {
        "id": 1,
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "summary": "A dystopian reality novel that focuses on the social aspects of the dangers behind technological advancements.",
        "year": 1932,
        "rating": 8,
        "read": True,
    },
    {
        "id": 2,
        "title": "100 years of solitude",
        "author": "Gabriel Garcia Marquez",
        "year": 1932,
        "rating": 8,
        "read": True,
    },
]


def find_book(id):
    for book in my_books:
        if book["id"] == id:
            return book

def find_index_book(id):
    for index, book in enumerate(my_books):
        if book['id'] == id:
            return index

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@app.get("/books")
def get_books():
    return {"books": my_books}

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_books(book: Book):
    book_dict = book.dict()
    book_dict['id'] = randrange(0, 100000)
    my_books.append(book_dict)
    return {"new_book": book_dict}

@app.get("/books/{id}")
def get_book(id: int, response: Response):
    book = find_book(id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"book with id {id} was not found",
        )
    return {"book_detail": book}

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_book(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"book with id {id} does not exist"
        )
    my_books.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/books/{id}")
def update_book(id: int, book: Book):
    print(book)
    index = find_index_book(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"book with id {id} does not exist"
        )
    book_dict = book.dict()
    book_dict['id'] = id
    my_books[index] = book_dict
    return {"data": book_dict}
