from redis import Redis as event_redis
from redis.asyncio import Redis as analyzer_redis
import json

class StatusStreamProducer:

    def __init__(
            self, 
            client: event_redis
        ) -> None:
        self._client = client


    def publish(
        self,
        stream_name: str,
        event: dict[str,str]
    ) -> int:
        event_id = self._client.rpush(
            stream_name,
            json.dumps(event)
        )

        return event_id


class EventsGenerationProducer:
    def __init__(
        self,
        client: analyzer_redis
    ) -> None:
        self._client = client

    def publish(
        self,
        stream_name: str,
        event: dict[str,str]
    ) -> int:

        return self._client.rpush(
            stream_name,
            json.dumps(event)
        )
        