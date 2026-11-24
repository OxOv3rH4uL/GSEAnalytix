from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Database URL is not present")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

local_session = sessionmaker(
    bind=engine,
    autoflush=False
)

class Base(DeclarativeBase):
    pass