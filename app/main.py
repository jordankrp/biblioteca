import os
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

# Load password from env variables
PASSWORD = os.environ['POSTGRES_PASSWORD']

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    summary: Optional[str] = None
    year: int
    rating: Optional[int] = None
    read: bool = False

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="bibliotecadb",
            user="postgres",
            password=PASSWORD,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connection to DB failed")
        print(f"Error: {error}")
        time.sleep(2)

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


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return {"data": books}


@app.get("/books")
def get_books(db: Session = Depends(get_db)):

    # cursor.execute(""" SELECT * FROM books """)
    # books = cursor.fetchall()

    books = db.query(models.Book).all()
    return {"books": books}


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_books(book: Book, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """ INSERT INTO books (title, author, summary, year) VALUES (%s, %s, %s, %s) RETURNING * """,
    #     (book.title, book.author, book.summary, book.year)
    # )
    # new_book = cursor.fetchone()
    # conn.commit()

    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"new_book": new_book}


@app.get("/books/{id}")
def get_book(id: int, db: Session = Depends(get_db)):

    # cursor.execute(""" SELECT * FROM books WHERE id = %s """, (str(id),))
    # book = cursor.fetchone()

    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"book with id {id} was not found",
        )
    return {"book_detail": book}


@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""  DELETE FROM books WHERE id = %s RETURNING * """, (str(id),))
    # deleted_book = cursor.fetchone()
    # conn.commit()

    book_query = db.query(models.Book).filter(models.Book.id == id)
    print(book_query)
    if book_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"book with id {id} does not exist"
        )
    book_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/books/{id}")
def update_book(id: int, updated_book: Book, db: Session = Depends(get_db)):
    
    # cursor.execute(
    #     """ UPDATE books SET title = %s, author = %s, year = %s, rating = %s, summary = %s, read = %s WHERE id = %s RETURNING * """,
    #     (book.title, book.author, book.year, book.rating, book.summary, book.read, str(id))    
    # )
    # updated_book = cursor.fetchone()
    # conn.commit()

    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()

    if book == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"book with id {id} does not exist"
        )
    book_query.update(updated_book.dict(), synchronize_session=False)

    db.commit()

    return {"data": book_query.first()}
