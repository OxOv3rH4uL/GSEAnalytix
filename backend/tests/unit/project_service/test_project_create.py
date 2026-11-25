#Unit test - Service while DB is mocked

import pytest
from app.schema.project_schema import ProjectCreateRequest, ProjectResponse
from app.core.exceptions import ProjectFoundError


class TestCreateProject:

    def test_project_success(
        self,
        project_service,
        mock_project_repo,
        mock_db,
        sample_project
    ):
        """
        Mocking the project repo and performing unit testing
        - Creating a successful project
        """
        data = ProjectCreateRequest(
            project_name="GSE"
        )

        """
        Project Service checks whether a project with that name exists or not via Project Repository
        Project Repo creates a project by communicating with the DB
        Simulating the same thing here
         
        """
        mock_project_repo.get_project_by_name.return_value = None
        mock_project_repo.create_project.return_value = sample_project


        result = project_service.create_project(data)

        """
        Validations
        """

        assert isinstance(result, ProjectResponse)
        assert result.project_id == sample_project.project_id
        assert result.project_name == data.project_name
        
        mock_project_repo.get_project_by_name.assert_called_once()
        mock_project_repo.create_project.assert_called_once()
        mock_db.commit.assert_called_once()
    

    def test_project_fail(
        self,
        project_service,
        mock_project_repo,
        mock_db,
        sample_project
    ):
        """
        Creating a duplicate project
        """
        data = ProjectCreateRequest(
            project_name="GSE"
        )

        """
        Simulating that a project with that name already exists
        """
        mock_project_repo.get_project_by_name.return_value = sample_project

        with pytest.raises(ProjectFoundError):
            project_service.create_project(data)

        mock_project_repo.create_project.assert_not_called()
        mock_db.commit.assert_not_called()




