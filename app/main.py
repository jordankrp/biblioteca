from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from . import models
from .database import engine
from .routers import book, user, auth, rating
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(rating.router)

@app.get("/", response_class=FileResponse)
def root():
    return FileResponse("static/index.html")


