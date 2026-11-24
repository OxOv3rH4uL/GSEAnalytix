from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.devices import DevicesDB
from decimal import Decimal
from uuid import UUID
from app.core.logger import get_logger

logger = get_logger(__name__)

class DeviceRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create_device(
        self,
        project_id: UUID,
        device_name: str,
        tariff_per_kwh: Decimal,
    ) -> DevicesDB:
        """
        Creating device for a project
        """
        logger.debug("Creating the device: %s for project with project_id: %s", device_name,project_id)
        device = DevicesDB(project_id=project_id, device_name=device_name, tariff_per_kwh=tariff_per_kwh)
        self._db.add(device)
        self._db.flush()
        return device

    def get_devices_by_project_id(
        self,
        project_id: UUID
    ) -> list[DevicesDB]:
        """
        Getting all devices that is used in the project
        """
        logger.debug("Getting all devices for the project with project_id: %s", project_id)

        query = select(DevicesDB).where(
            DevicesDB.project_id == project_id
        ).order_by(DevicesDB.created_at.desc())

        devices = list(self._db.scalars(query).all())
        return devices

    def get_device_by_name_and_project_id(
        self,
        project_id: UUID,
        device_name: str
    ) -> DevicesDB:
        """
        Getting device details based on device name and project_id
        """
        logger.debug("Getting device details for device_name:%s and project_id: %s", device_name,project_id)

        query = select(DevicesDB).where(
            DevicesDB.project_id == project_id,
            DevicesDB.device_name == device_name
        )
        device = self._db.execute(query).scalar_one_or_none()
        return device
    

    def get_device_by_id(
        self,
        device_id: UUID
    ) -> DevicesDB :
        """
        Get a device details by its device_id
        """
        logger.debug("Getting device details for device: %s", device_id)

        query = select(DevicesDB).where(
            DevicesDB.device_id == device_id
        )
        device = self._db.execute(query).scalar_one_or_none()
        return device

    def update_device(
        self,
        device_name: str,
        tariff_per_kwh: Decimal,
        device: DevicesDB
    ) -> DevicesDB | None:
        """
        Updating a device details
        """
        logger.debug("Updating device details for device_id: %s", device.device_id)
        
        device.device_name = device_name
        device.tariff_per_kwh = tariff_per_kwh
        self._db.flush()

        return device

    def delete_device(
        self,
        device: DevicesDB
    ) -> None:
        """
        Deleting a device
        """
        logger.debug("Deleting device with device_id: %s", device.device_id)
        self._db.delete(device)
        self._db.flush()


