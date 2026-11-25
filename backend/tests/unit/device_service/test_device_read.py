import pytest
from app.schema.device_schema import DeviceResponse
from app.core.exceptions import ProjectNotFoundError, DeviceNotFoundError
from uuid import uuid4


class TestReadDevice:

    def test_get_all_devices(
        self,
        device_service,
        mock_device_repo,
        mock_project_repo,
        sample_device,
        sample_project
    ):
        """
        Getting all devices by mocking the Device Repo and Project Repo
        """

        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_device_repo.get_devices_by_project_id.return_value = [
            sample_device
        ]

        result = device_service.get_devices_by_project_id(
            project_id=sample_project.project_id
        )

        assert isinstance(result,list)
        assert isinstance(result[0], DeviceResponse)
        assert result[0].project_id == sample_device.project_id
        assert result[0].device_id == sample_device.device_id
        assert result[0].device_name == sample_device.device_name

        mock_project_repo.get_project_by_id.assert_called_once()
        mock_device_repo.get_devices_by_project_id.assert_called_once()

    def test_get_device_by_id(
        self,
        device_service,
        mock_device_repo,
        sample_device
    ):
        """
        Getting device details based on device_id
        """
        mock_device_repo.get_device_by_id.return_value = sample_device

        result = device_service.get_device_by_id(
            device_id=sample_device.device_id
        )

        assert isinstance(result, DeviceResponse)
        assert result.device_id == sample_device.device_id
        mock_device_repo.get_device_by_id.assert_called_once()


    def test_get_device_fail_project_not_found(
        self,
        device_service,
        mock_device_repo,
        mock_project_repo,
    ):
        """
        Trying to get a device detail whose project doesnt exists
        """
        project_id = uuid4()

        mock_project_repo.get_project_by_id.return_value = None

        with pytest.raises(ProjectNotFoundError):
            device_service.get_devices_by_project_id(project_id=project_id)

        mock_project_repo.get_project_by_id.assert_called_once()
        mock_device_repo.get_devices_by_project_id.assert_not_called()


    def test_get_device_fail_device_not_found(
        self,
        device_service,
        mock_device_repo
    ):
        """
        Trying to retrieve the details of a device which doesnt exists
        """

        device_id = uuid4()
        mock_device_repo.get_device_by_id.return_value = None

        with pytest.raises(DeviceNotFoundError):
            device_service.get_device_by_id(device_id=device_id)

        mock_device_repo.get_device_by_id.assert_called_once()
        
