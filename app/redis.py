from redis_om import get_redis_connection
from .config import settings

redis_db = get_redis_connection(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT
)

