from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

logger = logging.getLogger(__name__)

engine = create_async_engine(
    "postgresql+asyncpg://devops:admin@db:5432/contacts_db", echo=True
)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db():
    async with async_session() as db:
        try:
            yield db
        except Exception as err:
            await db.rollback()
            logger.error(f"Database error: {str(err)}")
            raise
        finally:
            await db.close()


app = FastAPI()


@app.get("/test-db")
async def test_db(db=Depends(get_db)):
    # Perform a simple query or check
    return {"message": "Database connection is working!"}
