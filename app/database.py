from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


DATABASE_URL = f"postgresql://{settings.postgre_usr}:{settings.postgre_pwd}@{settings.postgre_host}:{settings.postgre_port}/{settings.database_name}"

engine = create_engine(DATABASE_URL)

local_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
base = declarative_base()


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
