from redis_lru import RedisLRU
import redis


client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)
cache = RedisLRU(client)


@cache
def compute_value(x):
    print(f"Function call compute_value({x})")
    return x**2
