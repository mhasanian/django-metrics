import redis
from django.conf import settings

REDIS_HOST = getattr(settings, "METRICS_REDIS_HOST", "localhost")
REDIS_PORT = getattr(settings, "METRICS_REDIS_PORT", 6379)

_redis_pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    max_connections=1000
)

redis_client = redis.Redis(connection_pool=_redis_pool)