import pytest
from app.core.exceptions import ProjectNotFoundError
from uuid import uuid4

class TestDeleteProject:

    def test_delete_project_success(
        self,
        project_service,
        mock_project_repo,
        mock_db,
        sample_project
    ):
        """
        Testing deleting a project
        """

        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_project_repo.delete_project.return_value = None

        result = project_service.delete_project(project_id=sample_project.project_id)

        assert result == None
        mock_project_repo.get_project_by_id.assert_called_once()
        mock_project_repo.delete_project.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_delete_project_fail_project_not_found(
        self,
        project_service,
        mock_project_repo,
        mock_db,
        sample_project
    ):
        """
        Simulating the deletion of a project whose id is not present
        """

        project_id = uuid4()
        mock_project_repo.get_project_by_id.return_value = None
        with pytest.raises(ProjectNotFoundError):
            project_service.delete_project(project_id=project_id)

        mock_project_repo.delete_project.assert_not_called()
        mock_db.commit.assert_not_called()
