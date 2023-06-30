from datetime import datetime
from typing import Sequence
from sqlalchemy import insert, select, update, desc, asc
from sqlalchemy.orm import Session
from sqlalchemy import exc
from commons.schemas import PostIn, Order

from commons.models import Post


class NotFoundError(Exception):
    pass


def get(limit: int, offset: int, order: Order, session: Session) -> Sequence[Post]:
    q = (
        select(Post)
        .where(Post.is_deleted == False)
        .order_by(
            desc(Post.published_at) if order is Order.DESC else asc(Post.published_at)
        )
        .limit(limit)
        .offset(offset)
    )
    return session.execute(q).scalars().all()


def get_one(post_id: int, session: Session) -> Post | None:
    q = select(Post).where(Post.is_deleted == False).where(Post.id == post_id)
    return session.execute(q).scalars().first()


def create(post_in: PostIn, session: Session) -> Post:
    q = (
        insert(Post)
        .values(
            updated_at=datetime.utcnow(),
            published_at=post_in.published_at,
            title=post_in.title,
            content=post_in.content,
            is_deleted=False,
        )
        .returning(Post)
    )
    post = session.execute(q).scalar_one()
    session.commit()
    return post


def update_(post_id: int, post_in: PostIn, session: Session) -> Post:
    q = (
        update(Post)
        .where(Post.id == post_id)
        .where(Post.is_deleted == False)
        .values(
            published_at=post_in.published_at,
            title=post_in.title,
            content=post_in.content,
        )
        .returning(Post)
    )
    try:
        post = session.execute(q).scalar_one()
    except exc.NoResultFound:
        raise NotFoundError

    session.commit()
    return post


def delete_(post_id: int, session: Session) -> None:
    q = (
        update(Post)
        .where(Post.id == post_id)
        .where(Post.is_deleted == False)
        .values(is_deleted=True)
        .returning(Post)
    )
    try:
        post = session.execute(q).scalar_one()
    except exc.NoResultFound:
        raise NotFoundError
    session.commit()
