from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.db.database import db

from core.models.drive import Drive
from core.models.user import User
from core.routes.drive import router as drive_router
from core.routes.user import router as user_router

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
