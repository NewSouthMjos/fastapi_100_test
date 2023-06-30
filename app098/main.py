from fastapi import FastAPI

from api.posts import router as posts_router


app = FastAPI(title='fastapi_test')


app.include_router(posts_router.router)
