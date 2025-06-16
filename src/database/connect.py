import redis.asyncio as redis
import logging

from redis_lru import RedisLRU
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.services.base import settings

logger = logging.getLogger(__name__)

client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)
cache = RedisLRU(client)

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    expire_on_commit=False,
    autoflush=False,
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


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
