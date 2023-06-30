from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from commons.database import get_db
from commons import schemas
from crud import posts


router = APIRouter(tags=["posts"])


@router.get("/posts")
def get_posts(
    per_page: int = 10,
    page: int = 0,
    order: schemas.Order = schemas.Order.DESC,
    session: Session = Depends(get_db),
) -> schemas.PostsOut:
    return schemas.PostsOut(posts=posts.get(per_page, per_page*page, order, session))


@router.get("/posts/{post_id}")
def get_post(post_id: int, session: Session = Depends(get_db)) -> schemas.PostOut:
    post = posts.get_one(post_id, session)
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return post


@router.post("/posts")
def create_post(
    post_in: schemas.PostIn, session: Session = Depends(get_db)
) -> schemas.PostOut:
    post = posts.create(post_in, session)
    return post


@router.put("/posts/{post_id}")
def update_post(
    post_id: int,
    post_in: schemas.PostIn,
    session: Session = Depends(get_db),
) -> schemas.PostOut:
    try:
        post = posts.update_(post_id, post_in, session)
    except posts.NotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return post


@router.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    session: Session = Depends(get_db),
) -> Response:
    try:
        posts.delete_(post_id, session)
    except posts.NotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_200_OK)
