import pytest
from app.core.exceptions import ProjectNotFoundError, DeviceNotFoundError
from uuid import uuid4


class TestDeleteDevice:

    def test_delete_device(
        self,
        device_service,
        mock_project_repo,
        mock_device_repo,
        sample_project,
        sample_device,
        mock_db
    ):
        """
        Testing deletion of a device in a project
        """

        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_device_repo.get_device_by_id.return_value = sample_device
        mock_device_repo.delete_device.return_value = None

        result = device_service.delete_device(
            project_id=sample_project.project_id,
            device_id = sample_device.device_name
        )

        assert result == None
        mock_project_repo.get_project_by_id.assert_called_once()
        mock_device_repo.get_device_by_id.assert_called_once()
        mock_device_repo.delete_device.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_delete_device_fail_project_not_found(
        self,
        device_service,
        mock_project_repo,
        mock_device_repo,
        sample_device,
        mock_db
    ):
        """
        Trying to delete a device whose project doesnt exist
        """

        project_id = uuid4()
        mock_project_repo.get_project_by_id.return_value = None

        with pytest.raises(ProjectNotFoundError):
            device_service.delete_device(
                project_id=project_id,
                device_id = sample_device.device_id
            )

        mock_device_repo.delete_device.assert_not_called()
        mock_db.commit.assert_not_called()


    def test_delete_device_fail_device_not_found(
        self,
        device_service,
        mock_project_repo,
        mock_device_repo,
        sample_project,
        mock_db
    ):
        """
        Trying to delete a device in a project which doesnt exist
        """

        device_id = uuid4()
        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_device_repo.get_device_by_id.return_value = None

        with pytest.raises(DeviceNotFoundError):
            device_service.delete_device(
                project_id=sample_project.project_id,
                device_id=device_id
            )

        mock_project_repo.get_project_by_id.assert_called_once()
        mock_device_repo.get_device_by_id.assert_called_once()
        mock_device_repo.delete_device.assert_not_called()
        mock_db.commit.assert_not_called()

    


    