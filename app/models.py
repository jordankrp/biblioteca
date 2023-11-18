from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Integer)
    summary = Column(String)
    read = Column(Boolean, default=False)