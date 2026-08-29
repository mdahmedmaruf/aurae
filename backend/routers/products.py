from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from dependencies import require_role
from models import Product, UserRole
from schemas import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


# Public: View Products
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    results = db.execute(select(Product))
    return results.scalars().all()


@router.post(
    "/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.ADMIN, UserRole.EDITOR))]
)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    product = product_data.model_dump(mode="json")

    new_product = Product(**product)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.patch(
    "/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(UserRole.ADMIN, UserRole.EDITOR))]
)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    result = db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    for field, val in product_data.model_dump(exclude_unset=True).items():
        setattr(product, field, val)

    db.commit()
    db.refresh(product)

    return product


@router.delete(
    "/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(UserRole.ADMIN))]
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(product)
    db.commit()
