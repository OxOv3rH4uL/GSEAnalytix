import pytest
from app.models.devices import DevicesDB
from app.schema.device_schema import DeviceUpdateRequest, DeviceResponse
from app.core.exceptions import ProjectNotFoundError, DeviceFoundError, DeviceNotFoundError
from decimal import Decimal
from uuid import uuid4
from datetime import datetime

class TestUpdateDevice:

    def test_update_device(
        self,
        device_service,
        mock_device_repo,
        mock_project_repo,
        sample_project,
        sample_device,
        mock_db
    ):
        """
        Simulating updation of a device
        """

        data = DeviceUpdateRequest(
            device_name="Generator Machinez",
            tariff_per_kwh= Decimal("19.9")   
        )

        updated_device = DevicesDB(
            device_id = sample_device.device_id,
            project_id = sample_device.project_id,
            device_name = data.device_name,
            tariff_per_kwh = data.tariff_per_kwh,
            status = sample_device.status,
            created_at = sample_device.created_at
        )

        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_device_repo.get_device_by_id.return_value = sample_device
        mock_device_repo.get_device_by_name_and_project_id.return_value = None
        mock_device_repo.update_device.return_value = updated_device

        result = device_service.update_device(
            project_id=sample_project.project_id,
            device_id=sample_device.device_id,
            data=data
        )

        assert isinstance(result,DeviceResponse)
        assert result.project_id == sample_device.project_id
        assert result.device_id == sample_device.device_id
        assert result.device_name == data.device_name
        assert result.tariff_per_kwh == data.tariff_per_kwh

        mock_project_repo.get_project_by_id.assert_called_once()
        mock_device_repo.get_device_by_name_and_project_id.assert_called_once()
        mock_device_repo.update_device.assert_called_once()
        mock_db.commit.assert_called_once()
        


    def test_update_device_fail_project_not_found(
        self,
        device_service,
        mock_project_repo,
        sample_device,
        mock_db
    ):
        """
        Simulating the updation of a device whose project is not found
        """
        data = DeviceUpdateRequest(
            device_name="Generator Machinez",
            tariff_per_kwh= Decimal("19.9")   
        )

        project_id = uuid4()
        mock_project_repo.get_project_by_id.return_value = None

        with pytest.raises(ProjectNotFoundError):
            device_service.update_device(
                project_id=project_id,
                device_id=sample_device,
                data=data
            )

        mock_project_repo.get_project_by_id.assert_called_once()
        mock_db.commit.assert_not_called()


    def test_update_device_fail_device_found(
        self,
        device_service,
        mock_project_repo,
        mock_device_repo,
        sample_device,
        sample_project,
        mock_db
    ):
        """
        Trying to update a device in a project whose updated details(device_name) already exists
        """

        data = DeviceUpdateRequest(
            device_name="Generator Machinez",
            tariff_per_kwh= Decimal("19.9")   
        )

        existing_device = DevicesDB(
            device_id = uuid4(),
            project_id = sample_project.project_id,
            device_name = data.device_name,
            tariff_per_kwh = data.tariff_per_kwh,
            status = sample_device.status,
            created_at = datetime.now()
        )

        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_device_repo.get_device_by_name_and_project_id.return_value = existing_device

        with pytest.raises(DeviceFoundError):
            device_service.update_device(
                project_id = sample_project.project_id,
                device_id = sample_device.device_id,
                data = data
            )

        mock_project_repo.get_project_by_id.assert_called_once()
        mock_device_repo.get_device_by_name_and_project_id.assert_called_once()
        mock_device_repo.update_device.assert_not_called()
        mock_db.commit.assert_not_called()


    def test_device_update_fail_device_not_found(
        self,
        device_service,
        mock_project_repo,
        mock_device_repo,
        sample_project,
        mock_db
    ):
        """
        Trying to update a device in a project which doesnt exist
        """
        data = DeviceUpdateRequest(
            device_name="Generator Machinez",
            tariff_per_kwh= Decimal("19.9")   
        )
        device_id = uuid4()

        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_device_repo.get_device_by_id.return_value = None

        with pytest.raises(DeviceNotFoundError):
            device_service.update_device(
                project_id=sample_project.project_id,
                device_id= device_id,
                data = data
            )

        mock_project_repo.get_project_by_id.assert_called_once()
        mock_device_repo.get_device_by_id.assert_called_once()
        mock_device_repo.update_device.assert_not_called()
        mock_db.commit.assert_not_called()



