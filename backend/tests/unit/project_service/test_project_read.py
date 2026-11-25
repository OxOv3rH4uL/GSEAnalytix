import pytest
from app.schema.project_schema import ProjectResponse
from app.core.exceptions import ProjectNotFoundError
from uuid import uuid4

class TestReadProject:
    def test_get_all_projects(
        self,
        project_service,
        mock_project_repo,
        mock_db,
        sample_project
    ):
        """
        Getting all projects by mocking the Project Repo
        """

        mock_project_repo.get_all_projects.return_value = [
            sample_project
        ]

        result = project_service.get_all_projects()

        assert isinstance(result,list)
        assert isinstance(result[0], ProjectResponse)
        assert result[0].project_id == sample_project.project_id
        assert result[0].project_name == sample_project.project_name
        assert mock_project_repo.get_all_projects.asset_called_once()


    def test_get_project_by_id_success(
        self,
        project_service,
        mock_project_repo,
        mock_db,
        sample_project
    ):
        """
        Getting a project based on id and simulation
        """

        mock_project_repo.get_project_by_id.return_value = sample_project

        result = project_service.get_project_by_id(project_id=sample_project.project_id)

        assert isinstance(result,ProjectResponse)
        assert result.project_id == sample_project.project_id
        assert result.project_name == sample_project.project_name
        mock_project_repo.get_project_by_id.assert_called_once()

        
    def test_get_project_by_id_not_found(
        self,
        project_service,
        mock_project_repo,
        mock_db
    ):
        """
        Simulating failure case where project_id is not found
        """

        project_id = uuid4()

        mock_project_repo.get_project_by_id.return_value = None

        with pytest.raises(ProjectNotFoundError):
            project_service.get_project_by_id(project_id=project_id)

    