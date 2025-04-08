from pydantic import BaseModel, EmailStr
from typing import Optional


class BaseUser(BaseModel):
    name: str
    email: EmailStr
    username: str



class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None