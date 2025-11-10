from typing import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base
from config import config

engine = create_engine(config.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()