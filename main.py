from fastapi import FastAPI, HTTPException
from db import init_db
from config import get_settings
from schemas.user import BaseUser, UserOut
from schemas.base import BaseResponse
from models.user import User
from contextlib import asynccontextmanager

settings = get_settings()


# Lifespan orqali startup event
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("DB Connected ✅")
    yield
    # Optional: shutdown uchun joy qoldirish mumkin


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI CRUD Tortoise ORM with Aerich",
    debug=settings.app_debug,
    lifespan=lifespan,
)


@app.get("/apps")
async def apps_ts() -> dict:
    return {"message": "apps"}


@app.get("/users", response_model=BaseResponse)
async def get_users():
    users = await User.all()
    user_list = [UserOut.model_validate(user) for user in users]
    return BaseResponse(status=True, data=user_list)


@app.post("/users", response_model=BaseResponse)
async def create_user(user: BaseUser):
    user_data = await User.create(
        name=user.name,
        email=user.email,
        username=user.username,
    )
    return BaseResponse(status=True, data=UserOut.model_validate(user_data))


@app.put("/users/{user_id}", response_model=BaseResponse)
async def update_user(user_id: int, user_data: BaseUser):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = user_data.name
    user.email = user_data.email
    user.username = user_data.username
    await user.save()

    return BaseResponse(status=True, data=UserOut.model_validate(user))


@app.delete("/users/{user_id}", response_model=BaseResponse)
async def delete_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return BaseResponse(status=True, data=f"User {user_id} deleted")
