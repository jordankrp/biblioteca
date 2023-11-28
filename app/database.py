import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load password from env variables
PASSWORD = os.environ['POSTGRES_PASSWORD']

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{PASSWORD}@localhost/bibliotecadb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
