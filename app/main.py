from fastapi import FastAPI
from . import models
from .database import engine
from .routers import book, user, auth, rating
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(rating.router)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}


