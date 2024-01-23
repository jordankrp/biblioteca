from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class BookBase(BaseModel):
    title: str
    author: str
    summary: Optional[str] = None
    year: int
    rating: Optional[int] = None
    read: bool = False

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None