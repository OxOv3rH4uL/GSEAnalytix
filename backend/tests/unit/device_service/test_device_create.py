import pytest
from app.schema.device_schema import DeviceCreateRequest, DeviceResponse
from app.core.exceptions import ProjectNotFoundError, DeviceFoundError
from app.models.devices import DevicesDB
from app.helpers.enums import DeviceStatus
from uuid import uuid4
from decimal import Decimal

class TestCreateDevice:

    def test_device_create(
        self,
        device_service,
        mock_device_repo,
        mock_project_repo,
        mock_db,
        sample_project,
        sample_device
    ):
        """
        Mocking the project and device repo and performing unit testing
        - Creating a successful device
        """

        data = DeviceCreateRequest(
            device_name = "Generator Machine",
            tariff_per_kwh=Decimal("20.9")
        )

        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_device_repo.get_device_by_name_and_project_id.return_value = None
        mock_device_repo.create_device.return_value = sample_device

        result = device_service.create_device(
            project_id=sample_project.project_id,
            data= data
        )

        """
        Validations
        """
        assert isinstance(result, DeviceResponse)
        assert result.project_id == sample_device.project_id
        assert result.device_id == sample_device.device_id
        assert result.device_name == data.device_name
        assert result.tariff_per_kwh == data.tariff_per_kwh

        mock_project_repo.get_project_by_id.assert_called_once()
        mock_device_repo.get_device_by_name_and_project_id.assert_called_once()
        mock_device_repo.create_device.assert_called_once()
        mock_db.commit.assert_called_once()


    def test_device_create_fail_project_not_found(
        self,
        device_service,
        mock_device_repo,
        mock_project_repo,
        mock_db
    ):
        """
        Trying to create a device with a project that doesnt exist
        """
        data = DeviceCreateRequest(
            device_name="Generator Machine",
            tariff_per_kwh=Decimal("20.9")
        )
        project_id = uuid4()

        mock_project_repo.get_project_by_id.return_value = None

        with pytest.raises(ProjectNotFoundError):
            device_service.create_device(
                project_id=project_id,
                data = data
            )

        mock_project_repo.get_project_by_id.assert_called_once()
        mock_device_repo.create_device.assert_not_called()
        mock_db.commit.assert_not_called()


    def test_device_create_fail_device_exists(
        self,
        device_service,
        mock_device_repo,
        mock_project_repo,
        sample_project,
        mock_db
    ):
        """
        Trying to create a device whose name already exists in that project
        """

        data = DeviceCreateRequest(
            device_name="Generator Machine",
            tariff_per_kwh=Decimal("20.9")
        )

        existing_device = DevicesDB(
            device_id = uuid4(),
            project_id = sample_project.project_id,
            device_name = data.device_name,
            tariff_per_kwh= Decimal("11.99")
        )

        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_device_repo.get_device_by_name_and_project_id.return_value = existing_device

        with pytest.raises(DeviceFoundError):
            device_service.create_device(
                project_id=sample_project.project_id,
                data = data
            )

        mock_project_repo.get_project_by_id.assert_called_once()
        mock_device_repo.get_device_by_name_and_project_id.assert_called_once()
        mock_device_repo.create_device.assert_not_called()
        mock_db.commit.assert_not_called()

    


        
    
