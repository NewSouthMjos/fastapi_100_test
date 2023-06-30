import os
from functools import lru_cache

from dataclasses import dataclass


@dataclass
class Settings:
    DATABASE_URL: str


@lru_cache
def get_settings() -> Settings:
    return Settings(DATABASE_URL=os.getenv('DATABASE_URL'))
