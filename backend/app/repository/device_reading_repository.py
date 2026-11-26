from sqlalchemy.orm import Session
from app.models.device_readings import DeviceReadings
from app.schema.device_reading_schema import DeviceReadingSchema
from app.repository.devices_repository import DeviceRepository
from app.core.exceptions import DeviceNotFoundError
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import get_logger


logger = get_logger(__name__)


class DeviceReadingRepository:

    def __init__(self,db: Session) -> None:
        self._db = db

    def create_device_reading(
        self,
        event: DeviceReadingSchema
    ) -> None:

        """
        Creating EventReadings and storing it in the event_reading table
        """
        device_repo = DeviceRepository(db=self._db)
        try:
            device = device_repo.get_device_by_id(
                device_id=event.device_id
            )

            if device is None:
                raise DeviceNotFoundError(f"Device with '{event.device_id}' not found")
            
            event = DeviceReadings(
                device_id= event.device_id,
                power_kw = event.power_kw,
                duration=  event.duration
            )
            self._db.add(event)
            self._db.commit()
            self._db.flush()

        except DeviceNotFoundError as e:
            self._db.rollback()
            logger.warning("Device not found!")
            raise

        except SQLAlchemyError as e:
            self._db.rollback()
            logger.warning("Getting database error")
            raise

        