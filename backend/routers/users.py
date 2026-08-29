from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from dependencies import require_role
from models import User, UserRole
from routers.security import hash_password
from schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.ADMIN, UserRole.EDITOR))]
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(UserRole.ADMIN))]
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
