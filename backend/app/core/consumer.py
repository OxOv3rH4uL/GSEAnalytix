from redis import Redis as event_redis
from redis.asyncio import Redis as analyzer_redis
import json

class StatusStreamConsumer:

    def __init__(
        self,
        client: analyzer_redis,
        stream_name: str
    ) -> None:
        self._client = client
        self._stream = stream_name

    async def consume(
        self
    ) -> dict:
        _ , event = await self._client.blpop(
            self._stream,
            timeout=0
        )

        return json.loads(event)


class EventStreamConsumer:

    def __init__(
        self,
        client: analyzer_redis,
        stream_name: str
    ) -> None:
        self._client = client
        self._stream = stream_name


    async def consume(
        self
    ) -> dict:

        _ , event = await self._client.blpop(
            self._stream,
            timeout=0
        )

        return json.loads(event)

        
        