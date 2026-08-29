from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from dependencies import require_role
from models import Category, UserRole
from schemas import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


# public: view categories
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    result = db.execute(select(Category))
    return result.scalars().all()


# admin and editor can create
@router.post(
    "/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.ADMIN, UserRole.EDITOR))]
    )
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**category_data.model_dump())

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


# only admin can delete category
@router.delete(
    "/{category_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(UserRole.ADMIN))]
    )
def delete_category(category_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(category)
    db.commit()
