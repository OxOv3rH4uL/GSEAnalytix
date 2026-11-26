import asyncio
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.exc import SQLAlchemyError
from app.repository.device_reading_repository import DeviceReadingRepository
from app.repository.device_analytics_repository import DeviceAnalyticsRepository
from app.repository.devices_repository import DeviceRepository
from app.schema.device_reading_schema import DeviceReadingSchema
from app.schema.device_analytics_schema import DeviceAnalyticsSchema
from app.core.consumer import EventStreamConsumer
from app.helpers.redis_client import redis_client_events
from app.helpers.db import local_session
from app.core.logger import get_logger
from app.core.exceptions import DeviceNotFoundError


logger = get_logger(__name__)

class AnalyticsWorker:

    def __init__(
        self,
        consumer: EventStreamConsumer
    ) -> None:
        self._consumer = consumer

    

    async def consume_events(
        self
    ) -> None:

        while True:
            event = await self._consumer.consume()
            print("event consumed")
            print(event)
            try:
                reading = DeviceReadingSchema.model_validate(event)

                await asyncio.to_thread(
                    self.process_events,
                    reading=reading
                )


            except Exception as e:
                logger.exception("Failed to process")

    def process_events(
        self,
        reading: DeviceReadingSchema
    ) -> None:
        """
        Here we gonna do 2 things
        1) Storing the incoming readings in the device_reading database
        2) Storing the processed analysis in the device_analytics database 
        """

        try:
            with local_session() as db:
                with db.begin():
                    device_reading_repo = DeviceReadingRepository(db=db)
                    analytics_repo = DeviceAnalyticsRepository(db=db)
                    devices_repo = DeviceRepository(db=db)
                    device = devices_repo.get_device_by_id(device_id=reading.device_id)

                    if device is None:
                        raise DeviceNotFoundError(f"Device with device_id: '{reading.device_id}' not found")
                    
                    device_reading = device_reading_repo.create_device_reading(
                        event=reading
                    )

                    total_energy = (
                        Decimal(str(reading.power_kw)) *
                        Decimal(str(reading.duration))
                    )
                    cost = (total_energy * device.tariff_per_kwh).quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP
                    )

                    analysis = DeviceAnalyticsSchema(
                        device_id = reading.device_id,
                        total_runtime = reading.duration,
                        total_kwh= total_energy,
                        total_cost= cost
                    )

                    analytics_repo.update_analysis(
                        event=analysis
                    )
                    
        except DeviceNotFoundError:
            logger.warning("Device with device id: %s not found", reading.device_id)

        except SQLAlchemyError:
            logger.exception("Getting database error")

    async def run_worker(
        self
    ) -> None:
        """
        Running the analytics worker
        """
        logger.info("Analytics Worker Started")

        async with asyncio.TaskGroup() as tasks:
            tasks.create_task(self.consume_events())


async def main():
    """
    Analytics Worker Main
    """

    consumer = EventStreamConsumer(
        client=redis_client_events,
        stream_name="device:readings"
    )

    analytics_worker = AnalyticsWorker(
        consumer=consumer
    )

    try:
        await analytics_worker.run_worker()

    except Exception as e:
        logger.exception("Some error occurred: %s", str(e))

    finally:
        await redis_client_events.aclose()

if __name__ == "__main__":
    asyncio.run(main())

    
    