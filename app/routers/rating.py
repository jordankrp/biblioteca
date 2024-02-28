from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix='/rating',
    tags=['Rating']
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def rate(
    rating: schemas.Rating,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    book = db.query(models.Book).filter(models.Book.id == rating.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {rating.book_id} was not found."
        )

    rating_query = db.query(models.Rating).filter(
        models.Rating.book_id == rating.book_id,
        models.Rating.user_id == current_user.id
    )

    rating_found = rating_query.first()

    if rating_found:
        # Update existing rating
        print("Rating found. Updating...")
        rating_found.rating = rating.score
        db.commit()
        return{"message": "Rating updated"}        

    # Create new rating  
    new_rating = models.Rating(
        book_id=rating.book_id,
        user_id=current_user.id,
        score=rating.score
    )

    db.add(new_rating)
    db.commit()
    return {"message": "Rating added successfully"}


@router.delete("/", status_code= status.HTTP_204_NO_CONTENT)
def rate(
    rating: schemas.RemoveRating,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    rating_query = db.query(models.Rating).filter(
        models.Rating.book_id == rating.book_id,
        models.Rating.user_id == current_user.id
    )

    rating_found = rating_query.first()

    if rating_found:
        # Delete existing rating
        print("Rating found. Deleting...")
        rating_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)     
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rating for book ID {rating.book_id} does not exist for current user."
        )