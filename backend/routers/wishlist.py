from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database import get_db
from dependencies import get_current_user
from models import Product, User, Wishlist
from schemas import WishlistResponse

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


# current customer wishlist
@router.get("/", response_model=list[WishlistResponse])
def get_wishlist(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = (select(Wishlist).options(selectinload(Wishlist.product)).where(Wishlist.user_id == current_user.id))
    wishlist = db.execute(stmt).scalars().all()

    return wishlist


# toggle product in wishlist
@router.post("/toggle/{product_id}", status_code=status.HTTP_200_OK)
def toggle_wishlist_item(product_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user), ):
    # verify product exits
    product_stmt = select(Product).where(Product.id == product_id)
    product_res = db.execute(product_stmt)
    if not product_res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # check wishlist status
    stmt = select(Wishlist).where(Wishlist.user_id == current_user.id, Wishlist.product_id == product_id)
    wishlist_item = db.execute(stmt).scalar_one_or_none()

    if wishlist_item:
        db.delete(wishlist_item)
        db.commit()
        return {"message": "Product removed from the wishlist"}
    else:
        new_wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.add(new_wishlist_item)
        db.commit()
        return {"message": "Product added to wishlist"}
