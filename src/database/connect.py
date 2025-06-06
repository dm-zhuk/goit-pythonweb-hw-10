"""Database Setup: sqlalchemy to define DB structure and connect to postgresql"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings.base import DB_USER, DB_PASSWORD, DB_DOMAIN, DB_NAME, DB_PORT
from .models import Base

# Database connection details
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_DOMAIN}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(url=DB_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables defined in models.py
Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
