from redis import Redis as event_redis
from redis.asyncio import Redis as analyzer_redis


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
    ) -> str:
        event_id = self._client.rpush(
            name=stream_name,
            fields=event
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
    ) -> str:

        return self._client.rpush(
            name= stream_name,
            fields = event
        )
        