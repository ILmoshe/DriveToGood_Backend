from fastapi import FastAPI

from .routes.user import router as user_router

app = FastAPI()

app.include_router(user_router, tags=["users"], prefix="/user")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}