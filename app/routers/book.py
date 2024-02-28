from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix='/books',
    tags=['Books']
)

@router.get("/", response_model=List[schemas.BookResponse])
def get_books(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):

    # cursor.execute(""" SELECT * FROM books """)
    # books = cursor.fetchall()
    print(limit)

    books = db.query(models.Book).filter(models.Book.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Book, func.count(models.Rating.book_id).label("number_of_ratings")).join(
        models.Rating,
        models.Rating.book_id == models.Book.id,
        isouter=True
    ).group_by(models.Book.id).all()

    print(results)

    return books


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BookResponse)
def create_books(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    # cursor.execute(
    #     """ INSERT INTO books (title, author, summary, year) VALUES (%s, %s, %s, %s) RETURNING * """,
    #     (book.title, book.author, book.summary, book.year)
    # )
    # new_book = cursor.fetchone()
    # conn.commit()

    new_book = models.Book(owner_id=current_user.id, **book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/{id}", response_model=schemas.BookResponse)
def get_book(id: int, db: Session = Depends(get_db)):

    # cursor.execute(""" SELECT * FROM books WHERE id = %s """, (str(id),))
    # book = cursor.fetchone()

    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"book with id {id} was not found",
        )
    return book


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    # cursor.execute("""  DELETE FROM books WHERE id = %s RETURNING * """, (str(id),))
    # deleted_book = cursor.fetchone()
    # conn.commit()

    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()

    if book == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"book with id {id} does not exist"
        )
    
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action."
                        )

    book_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.BookResponse)
def update_book(
    id: int,
    updated_book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    
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
    
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action."
                        )
    
    book_query.update(updated_book.dict(), synchronize_session=False)

    db.commit()

    return book_query.first()


