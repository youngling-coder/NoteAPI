from datetime import datetime
from typing import Optional
from pydantic import BaseModel, conint

class BaseUser(BaseModel):
    full_name: str
    username: str
    password: str


class CreateUser(BaseUser):
    pass


class LoginUser(BaseModel):
    username: str
    password: str


class ResponseUser(BaseModel):
    id: int
    full_name: str
    username: str

    class Config:
        from_attributes = True


class BaseTask(BaseModel):
    title: str
    detail: str
    priority: str


class CreateTask(BaseTask):
    pass


class Task(BaseTask):
    id: int
    timestamp: datetime
    owner: ResponseUser

    class Config:
        from_attributes = True


class ResponseTask(BaseModel):
    Task: Task


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
