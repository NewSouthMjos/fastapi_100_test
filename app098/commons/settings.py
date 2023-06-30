from functools import lru_cache

from pydantic import BaseSettings, ValidationError


class Settings(BaseSettings):
    DATABASE_URL: str


@lru_cache
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        print('FAULT WHILE LOADING EVNS:')
        raise e
