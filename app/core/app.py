from beanie import init_beanie
from fastapi import Depends, FastAPI, middleware
from fastapi.middleware.cors import CORSMiddleware

from .database import db
# from .user.schemas import UserCreate, UserRead, UserUpdate
# from .user.users import auth_backend, current_active_user, fastapi_users

from .models.drive import Drive
from .models.user import User
from .routes.drive import router as drive_router
from .routes.user import router as user_router

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            Drive,
            User,
        ],
    )


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


# DRIVE ROUTER
app.include_router(drive_router, tags=["drive"])

# USER ROUTER
app.include_router(user_router, tags=["user"])
