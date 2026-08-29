from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl

from models import UserRole


# -- User Schemas --
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.CUSTOMER


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


# -- Category Schemas --
class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None
    description: str | None = None


class CategoryResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


# -- Review Schemas --
class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating scale between 1 and 5")
    comment: str


class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# -- Product Schemas --
class ProductImageResponse(BaseModel):
    id: int
    url: str
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    stock: int
    image_url: HttpUrl
    category_id: int | None = None


class ProductUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    image_url: HttpUrl | None = None
    category_id: int | None = None


class ProductResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    stock: int
    image_url: str
    images: list[ProductImageResponse] = []
    category: CategoryResponse | None = None
    average_rating: float = 0.0
    total_reviews: int = 0
    model_config = ConfigDict(from_attributes=True)


# -- Wishlist Schemas --
class WishlistResponse(BaseModel):
    id: int
    product: ProductResponse
    model_config = ConfigDict(from_attributes=True)
