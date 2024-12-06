import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from contextlib import contextmanager

DATABASE_URL = "mysql+pymysql://root@localhost:3306/FastAPI_LMS"
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"}, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()