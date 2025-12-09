from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    score: Optional[int] = None
    feedback: Optional[str] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    status: str
    score: Optional[int] = None
    feedback: Optional[str] = None
    owner_id: int

    class Config:
        orm_mode = True