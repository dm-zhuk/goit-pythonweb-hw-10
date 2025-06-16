import redis.asyncio as redis
from src.services.base import settings


r = redis.from_url(settings.REDIS_URL)


def get_r_client() -> redis.Redis:
    """Dependency to get the Redis client."""
    return r
