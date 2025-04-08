from fastapi import FastAPI, HTTPException
from db import init_db
from config import get_settings
from schemas.user import BaseUser, UpdateUser
from schemas.base import BaseResponse
from models.user import User

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI CRUD Tortoise-orm with aerich",
    debug=settings.app_debug,
)


@app.on_event("startup")
async def startup():
    await init_db()
    print("DB Connected ✅")


# Create
@app.post("/user", response_model=BaseResponse)
async def create_user(user: BaseUser):
    user_data = await User.create(
        name=user.name,
        email=user.email,
        username=user.username
    )

    data = {
        "name": user_data.name,
        "email": user_data.email,
        "username": user_data.username
    }
    return BaseResponse(data=data)


# Read
@app.get("/user/{user_id}", response_model=BaseResponse)
async def get_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    data = {
        "name": user.name,
        "email": user.email,
        "username": user.username
    }
    return BaseResponse(data=data)


# Update
@app.put("/user/{user_id}", response_model=BaseResponse)
async def update_user(user_id: int, user: UpdateUser):
    user_obj = await User.get_or_none(id=user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")

    user_obj.name = user.name or user_obj.name
    user_obj.email = user.email or user_obj.email
    user_obj.username = user.username or user_obj.username
    await user_obj.save()

    data = {
        "name": user_obj.name,
        "email": user_obj.email,
        "username": user_obj.username
    }
    return BaseResponse(data=data)


# Delete
@app.delete("/user/{user_id}", response_model=BaseResponse)
async def delete_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return BaseResponse(data=f"User with id {user_id} deleted successfully")
