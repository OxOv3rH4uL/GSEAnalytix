import os
from dotenv import load_dotenv
from redis import Redis as event_redis
from redis.asyncio import Redis as analyzer_redis


load_dotenv()

REDIS_URL_STATUS = os.getenv("REDIS_URL_STATUS")
REDIS_URL_EVENTS = os.getenv("REDIS_URL_EVENTS")

redis_client_status = event_redis.from_url(
    REDIS_URL_STATUS,
    decode_responses = True,
    socket_timeout = None,
    socket_connect_timeout=5
)

redis_client_status_consumer = analyzer_redis.from_url(
    REDIS_URL_STATUS,
    decode_responses = True,
    socket_timeout = None,
    socket_connect_timeout=5
)

redis_client_events = analyzer_redis.from_url(
    REDIS_URL_EVENTS,
    decode_responses = True,
    socket_timeout = None,
    socket_connect_timeout=5
)

