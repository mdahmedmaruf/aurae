from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import Product, Review, User, UserRole
from schemas import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/products/{product_id}/reviews", tags=["Reviews"])


# public: list reviews for a specific product
@router.get("/", response_model=list[ReviewResponse])
def list_product_reviews(product_id: int, db: Session = Depends(get_db)):
    stmt = select(Review).where(Review.product_id == product_id)
    reviews = db.execute(stmt).scalars().all()

    return reviews


# logged in customer: add or update review
@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(product_id: int, review_data: ReviewCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    # verify product exists
    product_res = db.execute(select(Product).where(Product.id == product_id)).scalar_one_or_none()

    if not product_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # check for existing review
    stmt = select(Review).where(Review.product_id == product_id, Review.user_id == current_user.id)
    existing_review = db.execute(stmt).scalar_one_or_none()
    if existing_review:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already reviewed this product")

    review = Review(**review_data.model_dump(), product_id=product_id, user_id=current_user.id)

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


# delete review (owner or admin)
@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(product_id: int, review_id: int, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    stmt = select(Review).where(Review.id == review_id, Review.product_id == product_id)
    review = db.execute(stmt).scalar_one_or_none()

    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    # access control must be owner or admin
    if review.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this review"
            )

    db.delete(review)
    db.commit()
