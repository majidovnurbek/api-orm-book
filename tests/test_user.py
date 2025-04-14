import pytest
from httpx import AsyncClient
from main import app
from models.user import User

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/user", json={
            "name": "Test Name",
            "email": "test@example.com",
            "username": "testuser"
        })
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Test Name"
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

@pytest.mark.asyncio
async def test_get_user():
    user = await User.create(name="Get User", email="get@example.com", username="getuser")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/user/{user.id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Get User"

@pytest.mark.asyncio
async def test_update_user():
    user = await User.create(name="Old Name", email="old@example.com", username="olduser")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/user/{user.id}", json={
            "name": "New Name"
        })
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "New Name"
    assert data["email"] == "old@example.com"

@pytest.mark.asyncio
async def test_delete_user():
    user = await User.create(name="Delete Me", email="delete@example.com", username="deleteuser")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/user/{user.id}")
    assert response.status_code == 200
    msg = response.json()["data"]
    assert f"User with id {user.id} deleted successfully" in msg

    user_check = await User.get_or_none(id=user.id)
    assert user_check is None
