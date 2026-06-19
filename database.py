import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USE_SQLITE = os.getenv("USE_SQLITE", "True").lower() == "true"

if USE_SQLITE:
    DATABASE_URL = "sqlite:///./tasks.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "taskmanager")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
