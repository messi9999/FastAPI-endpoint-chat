import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy.orm import Session
from models.models import Base

from dotenv import load_dotenv

load_dotenv()

username = os.getenv("dbUsername")
password = os.getenv("dbPassword")
host = os.getenv("dbHost")
port = os.getenv("dbPort")
dbname = os.getenv("dbName")

# database_url = "postgresql://postgres:1234@localhost:5432/ArticalChat"

database_url = "postgresql://{}:{}@{}:{}/{}".format(
    username, password, host, port, dbname
)
database = Database(database_url)
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
