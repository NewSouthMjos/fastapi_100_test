from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from commons.settings import get_settings


settings = get_settings()

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as session:
        yield session
