from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, computed_field


class PostOut(BaseModel):
    id: int
    published_at: datetime
    updated_at: datetime
    title: str
    content: str

    @computed_field
    @property
    def is_published(self) -> bool:
        return datetime.utcnow() >= self.published_at

    class Config:
        from_attributes = True


class PostsOut(BaseModel):
    posts: list[PostOut]


class PostIn(BaseModel):
    title: str
    content: str
    published_at: datetime


class Order(StrEnum):
    ASC = "asc"
    DESC = "desc"
