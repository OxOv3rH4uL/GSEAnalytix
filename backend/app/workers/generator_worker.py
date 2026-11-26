import asyncio
from app.repository.devices_repository import DeviceRepository
from app.core.consumer import StatusStreamConsumer
from app.core.producer import EventsGenerationProducer
from app.helpers.enums import DeviceStatus
from app.helpers.redis_client import redis_client_status_consumer, redis_client_events
from app.helpers.db import local_session
from uuid import UUID
import random
from collections import deque
from app.core.logger import get_logger

logger = get_logger(__name__)


class EventGeneratorWorker:

    def __init__(
        self,
        consumer: StatusStreamConsumer,
        producer: EventsGenerationProducer
    ) -> None:
        self._consumer = consumer
        self._producer = producer
        self._queue : deque[str] = deque()
        self._interval = 0.2


    def update_device_status(
        self,
        device_id: str,
        status : str
    ) -> None:
        """
        Updates the status of a device
         - running
         - stopped
        """
        with local_session() as db:

            device_repo = DeviceRepository(db)
            device_repo.update_device_status(
                device_id=UUID(device_id),
                status=DeviceStatus(status)
            )

    def generate_readings(
        self,
        device_id: str
    ) -> dict[str,str]:
        """
        Generates a mocked reading for the device for analysis
        """
        return {
            "device_id" : device_id,
            "power_kw" : round(random.uniform(1,10),3),
            "duration" : round(random.uniform(0.5,5),2)
        }

    async def listen_for_status(
            self
        ) -> None:
        """
        Listen for events by consuming and pushes to the queue
        """
        while True:
            event = await self._consumer.consume()

            device_id = event["device_id"]
            status = event["status"]

            try:
                await asyncio.to_thread(
                    self.update_device_status,
                    device_id=device_id,
                    status=status
                )

                if status == "running":
                    if device_id not in self._queue:
                        self._queue.append(device_id)

                elif status == "stopped":
                    if device_id in self._queue:
                        self._queue.remove(device_id)    

            except Exception as e:
                logger.exception("Failed to process device_id: %s causing Exception : %s" , device_id, str(e))

    
    async def event_generation(
        self
    ) -> None:
        while True:

            start_time = asyncio.get_running_loop().time()

            for i in range(len(self._queue)):

                """
                If queue is empty
                """
                if not self._queue:
                    break

                device_id = self._queue.popleft()

                reading = self.generate_readings(device_id=device_id)
                self._queue.append(device_id)

                await self._producer.publish(
                    stream_name="device:readings",
                    event = reading
                )


            taken_time = asyncio.get_running_loop.time() - start_time

            await asyncio.sleep(
                max(0,self._interval-taken_time)
            )

    async def run_worker(
        self
    ) -> None:
        """
        Creating the tasks using asyncio and running them
        """
        logger.info("Event Generation Worker Started")

        async with asyncio.TaskGroup() as tasks:
            tasks.create_task(self.listen_for_status())
            tasks.create_task(self.event_generation())


async def main():

    """
    Event Generation Worker Main
    """

    consumer = StatusStreamConsumer(
        client=redis_client_status_consumer,
        stream_name="device:status"
    )

    producer = EventsGenerationProducer(
        client=redis_client_events,
    )

    event_worker = EventGeneratorWorker(
        consumer=consumer,
        producer=producer
    )


    try:
        await event_worker.run_worker()

    except Exception as e:
        logger.exception("Some error occurred: %s", str(e))

    finally:
        await redis_client_status_consumer.aclose()
        await redis_client_events.aclose()


if __name__ == "__main__":
    asyncio.run(main())



