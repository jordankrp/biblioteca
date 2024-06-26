from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import book, user, auth, rating
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(rating.router)

@app.get("/")
def root():
    return {"message": "Welcome to Biblioteca API. Code deployed through Github Actions."}


