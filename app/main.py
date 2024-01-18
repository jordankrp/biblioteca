import os
from typing import List
from fastapi import FastAPI, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import book, user, auth

# Load password from env variables
PASSWORD = os.environ['POSTGRES_PASSWORD']

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}


