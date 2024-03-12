from typing import Optional
from typing_extensions import Annotated
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint


class BookBase(BaseModel):
    title: str
    author: str
    summary: Optional[str] = None
    year: int

class BookCreate(BookBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class BookResponse(BookBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class BookResponseWithRatings(BaseModel):
    Book: BookResponse
    average_rating: float | None
    number_of_ratings: int | None

    class Config:
        orm_mode = True
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Rating(BaseModel):
    book_id: int
    score: int

class RemoveRating(BaseModel):
    book_id: int
