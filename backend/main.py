from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import User, UserRole
from routers import auth, categories, products, reviews, users, wishlist
from routers.security import hash_password


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Create tables on startup
    Base.metadata.create_all(bind=engine)

    # 2. Seed initial system users
    with SessionLocal() as db:
        stmt = select(User).where(User.id == 1)
        res = db.execute(stmt)

        if not res.scalar_one_or_none():
            admin_user = User(
                id=1,
                username="admin_user",
                email="admin@shop.com",
                password=hash_password("admin123"),
                role=UserRole.ADMIN,
            )
            editor_user = User(
                id=2,
                username="editor_user",
                email="editor@shop.com",
                password=hash_password("editor123"),
                role=UserRole.EDITOR,
            )
            customer_user = User(
                id=3,
                username="customer_user",
                email="customer@shop.com",
                password=hash_password("customer123"),
                role=UserRole.CUSTOMER,
            )

            db.add_all([admin_user, editor_user, customer_user])
            db.commit()

    yield


app = FastAPI(title="AURAE E-Commerce API", lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(wishlist.router)
app.include_router(reviews.router)


@app.get("/")
def home():
    return {"message": "Welcome to AURAE Products API"}
