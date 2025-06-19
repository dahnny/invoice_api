from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database_name
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)