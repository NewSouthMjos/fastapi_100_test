from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, validator


class PostOut(BaseModel):
    id: int
    published_at: datetime
    updated_at: datetime
    title: str
    content: str
    is_published: bool | None = None

    @validator("is_published", always=True)
    def compute_is_published(cls, v, values, **kwargs):
        return datetime.utcnow() >= values["published_at"]

    class Config:
        orm_mode = True


class PostsOut(BaseModel):
    posts: list[PostOut]


class PostIn(BaseModel):
    title: str
    content: str
    published_at: datetime


class Order(StrEnum):
    ASC = "asc"
    DESC = "desc"
