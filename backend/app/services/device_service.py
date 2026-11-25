from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.repository.devices_repository import DeviceRepository
from app.repository.projects_repository import ProjectRepository
from app.schema.device_schema import DeviceCreateRequest, DeviceUpdateRequest, DeviceResponse
from app.core.exceptions import DeviceFoundError, DeviceNotFoundError, ProjectNotFoundError, DatabaseError
from uuid import UUID
from app.core.logger import get_logger

logger = get_logger(__name__)

class DeviceService:
    """
    Application Logic of Device Service
    """

    def __init__(
        self,
        db: Session,
        project_repo: ProjectRepository,
        device_repo: DeviceRepository
    ) -> None:
        self._db = db
        self._project_repo = project_repo
        self._device_repo = device_repo

    def create_device(
        self,
        project_id: UUID,
        data: DeviceCreateRequest
    ) -> DeviceResponse:
        """
        Creating a device for a project
        """
        try:
            project_exists = self._project_repo.get_project_by_id(project_id=project_id)
            if project_exists is None:
                raise ProjectNotFoundError(
                    f"Project with project_id: '{project_id}' not found"
                )
            device_exists = self._device_repo.get_device_by_name_and_project_id(project_id=project_id,device_name=data.device_name)
            if device_exists is not None:
                raise DeviceFoundError(
                    f"Device with name: '{data.device_name}' already exists"
                )
            device = self._device_repo.create_device(project_id=project_id, device_name=data.device_name, tariff_per_kwh=data.tariff_per_kwh)
            res = DeviceResponse.model_validate(device)
            self._db.commit()

            logger.info("Device created successfully with device_id: %s", res.device_id)
            return res
        
        except ProjectNotFoundError:
            logger.warning("Project with project_id: %s not exists",project_id)
            self._db.rollback()
            raise

        except DeviceFoundError:
            logger.warning("Device with name: %s already exists", data.device_name)
            self._db.rollback()
            raise

        except SQLAlchemyError:
            self._db.rollback()
            logger.exception("Getting Database Error")
            raise DatabaseError("Failed to create device")

    def create_device_by_project_name(
        self,
        project_name: str,
        data: DeviceCreateRequest
    ) -> DeviceResponse:
        """
        Creating a device for a project based on project_name
        """
        try:
            project_exists = self._project_repo.get_project_by_name(project_name=project_name)
            if project_exists is None:
                raise ProjectNotFoundError(
                    f"Project with project_name: '{project_name}' not found"
                )
            device_exists = self._device_repo.get_device_by_name_and_project_name(device_name=data.device_name, project_name=project_name)
            if device_exists is not None:
                raise DeviceFoundError(
                    f"Device with name: '{data.device_name}' already exists"
                )
            device = self._device_repo.create_device(project_id=project_exists.project_id,device_name=data.device_name,tariff_per_kwh=data.tariff_per_kwh)
            res = DeviceResponse.model_validate(device)
            self._db.commit()

            logger.info("Device created successfully with device_id: %s", res.device_id)
            return res

        except ProjectNotFoundError:
            logger.warning("Project with project_name: %s not exists",project_name)
            self._db.rollback()
            raise

        except DeviceFoundError:
            logger.warning("Device with name: %s already exists", data.device_name)
            self._db.rollback()
            raise

        except SQLAlchemyError:
            self._db.rollback()
            logger.exception("Getting Database Error")
            raise DatabaseError("Failed to create device")

    def get_devices_by_project_id(
        self,
        project_id: UUID
    ) -> list[DeviceResponse]:
        """
        Getting all devices based on project_id
        """

        try:
            project_exists = self._project_repo.get_project_by_id(project_id=project_id)
            if project_exists is None:
                raise ProjectNotFoundError(
                    f"Project with project_id: '{project_id}' not found"
                )
            devices = self._device_repo.get_devices_by_project_id(project_id=project_id)
            res = [DeviceResponse.model_validate(device) for device in devices]
            logger.info("Getting all devices based on project_id: %s", project_id)
            return res
        

        except ProjectNotFoundError:
            logger.warning("Project with project_id: %s not exists",project_id)
            self._db.rollback()
            raise

        except SQLAlchemyError:
            self._db.rollback()
            logger.exception("Getting Database Error")
            raise DatabaseError("Failed to get device details")

    def get_device_by_name_and_project_name(
        self,
        project_name: str,
        device_name: str
    ) -> DeviceResponse:
        """
        Getting a device details based on device_name and project_name
        """
        try:
            project_exists = self._project_repo.get_project_by_name(project_name=project_name)
            if project_exists is None:
                raise ProjectNotFoundError(
                    f"Project with project_name: '{project_name}' not found"
                )

            device_exists = self._device_repo.get_device_by_name_and_project_name(project_name=project_name,device_name=device_name)
            if device_exists is None:
                raise DeviceNotFoundError(
                    f"Device with the name: '{device_name}' in the project: {project_name} not found"
                )
            res = DeviceResponse.model_validate(device_exists)
            logger.info("Getting device details of device_name: %s in project: %s", device_name, project_name)

            return res

        except ProjectNotFoundError:
            logger.warning("Project with project_name: %s not exists",project_name)
            self._db.rollback()
            raise

        except DeviceNotFoundError:
            logger.warning("Device with device_name: %s not found", device_name)
            self._db.rollback()
            raise

        except SQLAlchemyError:
            self._db.rollback()
            logger.exception("Getting Database Error")
            raise DatabaseError("Failed to get device details")

    def get_device_by_id(
        self,
        device_id: UUID
    ) -> DeviceResponse:
        """
        Getting device details based on device_id
        """
        try:
            device_exists = self._device_repo.get_device_by_id(device_id=device_id)
            if device_exists is None:
                raise DeviceNotFoundError(
                    f"Device with the device_id: '{device_id}' not found"
                )
            res = DeviceResponse.model_validate(device_exists)
            logger.info("Getting device details with device_id: %s", device_id)

            return res

        except DeviceNotFoundError:
            logger.warning("Device with device_id: %s not found", device_id)
            self._db.rollback()
            raise
        except SQLAlchemyError:
            self._db.rollback()
            logger.exception("Getting Database Error")
            raise DatabaseError("Failed to get device details")

    def update_device(
        self,
        project_id: UUID,
        device_id: UUID,
        data: DeviceUpdateRequest 
    ) -> DeviceResponse:
        """
        Update device details
        """
        try:
            existing_project = self._project_repo.get_project_by_id(project_id=project_id)
            if existing_project is None:
                raise ProjectNotFoundError(f"Project with project_id: {project_id} not found")
            existing_device = self._device_repo.get_device_by_id(device_id=device_id)
            if existing_device is None:
                raise DeviceNotFoundError(f"Device with device_id: '{device_id}' not found")

            device_ = self._device_repo.get_device_by_name_and_project_id(device_name=data.device_name, project_id=project_id)
            if(device_ is not None and device_.device_id != device_id):
                raise DeviceFoundError(f"Device with device_name: '{data.device_name}' already exists")

            updated_device = self._device_repo.update_device(device_name=data.device_name,tariff_per_kwh=data.tariff_per_kwh,device=existing_device)
            res = DeviceResponse.model_validate(updated_device)
            self._db.commit()
            logger.info("Device with device_id: %s updated successfully", device_id)
            return res

        except ProjectNotFoundError:
            logger.warning("Project with project_id: %s not exists",project_id)
            self._db.rollback()
            raise

        except DeviceFoundError:
            logger.warning("Device with name: %s already exists", data.device_name)
            self._db.rollback()
            raise

        except DeviceNotFoundError:
            logger.warning("Device with device_id: %s not found", device_id)
            self._db.rollback()
            raise

        except SQLAlchemyError:
            self._db.rollback()
            logger.exception("Getting Database Error")
            raise DatabaseError("Failed to update device")

    def update_device_by_name(
        self,
        project_name: str,
        device_name: str,
        data: DeviceUpdateRequest
    ) -> DeviceResponse:
        """
        Update device details based on project_name and device_name
        """
        try:
            existing_project = self._project_repo.get_project_by_name(project_name=project_name)
            if existing_project is None:
                raise ProjectNotFoundError(f"Project with project_name: {project_name} not found")
            existing_device = self._device_repo.get_device_by_name_and_project_name(project_name=project_name, device_name=device_name)
            if existing_device is None:
                raise DeviceNotFoundError(f"Device with device_name: '{device_name}' not found")
            device_ = self._device_repo.get_device_by_name_and_project_name(project_name=project_name, device_name=data.device_name)
            if (device_ is not None and device_.device_id != existing_device.device_id):
                raise DeviceFoundError(f"Device with device_name: '{data.device_name}' already exists")

            updated_device = self._device_repo.update_device(device_name=data.device_name,tariff_per_kwh=data.tariff_per_kwh,device=existing_device)
            res = DeviceResponse.model_validate(updated_device)
            self._db.commit()

            logger.info("Device with device_id: %s updated successfully", res.device_id)
            return res

        except ProjectNotFoundError:
            logger.warning("Project with project_name: %s not exists",project_name)
            self._db.rollback()
            raise

        except DeviceNotFoundError:
            logger.warning("Device with device_name: %s not found", device_name)
            self._db.rollback()
            raise

        except DeviceFoundError:
            logger.warning("Device with name: %s already exists", data.device_name)
            self._db.rollback()
            raise

        except SQLAlchemyError:
            self._db.rollback()
            logger.exception("Getting Database Error")
            raise DatabaseError("Failed to update device")

    def delete_device(
        self,
        device_id : UUID,
        project_id : UUID
    ) -> None:
        """
        Deleting a device
        """
        try:
            existing_project = self._project_repo.get_project_by_id(project_id=project_id)
            if existing_project is None:
                raise ProjectNotFoundError(f"Project with project_id: {project_id} not found")
            existing_device = self._device_repo.get_device_by_id(device_id=device_id)
            if existing_device is None:
                raise DeviceNotFoundError(f"Device with device_id: '{device_id}' not found")

            self._device_repo.delete_device(device=existing_device)
            self._db.commit()

            logger.info("Device with device_id: %s in project_id: %s deleted successfully", device_id, project_id)
            
        except ProjectNotFoundError:
            logger.warning("Project with project_id: %s not exists",project_id)
            self._db.rollback()
            raise

        except DeviceNotFoundError:
            logger.warning("Device with device_id: %s not found", device_id)
            self._db.rollback()
            raise

        except SQLAlchemyError:
            self._db.rollback()
            logger.exception("Getting Database Error")
            raise DatabaseError("Failed to delete device")

    def delete_device_by_name(
        self,
        device_name : str,
        project_name: str
    ) -> None:
        """
        Deleting a device based on device_name, project_name
        """
        try:
            existing_project = self._project_repo.get_project_by_name(project_name=project_name)
            if existing_project is None:
                raise ProjectNotFoundError(f"Project with project_name: {project_name} not found")
            existing_device = self._device_repo.get_device_by_name_and_project_name(project_name=project_name, device_name=device_name)
            if existing_device is None:
                raise DeviceNotFoundError(f"Device with device_name: '{device_name}' not found")

            self._device_repo.delete_device(device=existing_device)
            self._db.commit()

            logger.info("Device with device_name: %s deleted successfully",device_name)

            
        except ProjectNotFoundError:
            logger.warning("Project with project_name: %s not exists",project_name)
            self._db.rollback()
            raise

        except DeviceNotFoundError:
            logger.warning("Device with device_name: %s not found", device_name)
            self._db.rollback()
            raise

        except SQLAlchemyError:
            self._db.rollback()
            logger.exception("Getting Database Error")
            raise DatabaseError("Failed to delete device")