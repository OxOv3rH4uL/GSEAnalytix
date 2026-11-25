import pytest
from app.models.projects import ProjectsDB
from app.schema.project_schema import ProjectUpdateRequest, ProjectResponse
from app.core.exceptions import ProjectNotFoundError, ProjectFoundError, DatabaseError
from uuid import uuid4
from datetime import datetime

class TestUpdateProject:

    def test_update_project_success(
        self,
        project_service,
        mock_project_repo,
        mock_db,
        sample_project
    ):
        """
        Simulating updation of a project
        """

        data = ProjectUpdateRequest(
            project_name="GSE Updatign"
        )

        updated_project = ProjectsDB(
            project_id = sample_project.project_id,
            project_name = data.project_name,
            created_at = sample_project.created_at
        )

        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_project_repo.get_project_by_name.return_value = None
        mock_project_repo.update_project.return_value = updated_project

        result = project_service.update_project(
            project_id=sample_project.project_id,
            data=data
        )

        assert isinstance(result, ProjectResponse)
        assert result.project_name == data.project_name
        assert result.project_id == sample_project.project_id
        mock_project_repo.get_project_by_id.assert_called_once()
        mock_project_repo.get_project_by_name.assert_called_once()
        mock_project_repo.update_project.assert_called_once()
        mock_db.commit.assert_called_once()


    def test_update_project_fail_project_not_found(
        self,
        project_service,
        mock_project_repo,
        mock_db,
        sample_project
    ):
        """
        Simulating the updation of an invalid project
        """

        data = ProjectUpdateRequest(
            project_name="GSE Updating"
        )
        
        project_id = uuid4()
        mock_project_repo.get_project_by_id.return_value = None

        with pytest.raises(ProjectNotFoundError):
            project_service.update_project(project_id=project_id, data=data)

        mock_project_repo.update_project.assert_not_called()
        mock_db.commit.assert_not_called()

    def test_update_project_fail_name_exists(
        self,
        project_service,
        mock_project_repo,
        mock_db,
        sample_project
    ):
        """
        Simulating the updation of a project whose new name already exists
        """

        data = ProjectUpdateRequest(
            project_name="GSE"
        )

        updating_project = ProjectsDB(
            project_id = uuid4(),
            project_name = data.project_name,
            created_at = datetime.now()
        )

        mock_project_repo.get_project_by_id.return_value = sample_project
        mock_project_repo.get_project_by_name.return_value = updating_project

        with pytest.raises(ProjectFoundError):
            project_service.update_project(
                project_id=sample_project.project_id,
                data = data
            )

        mock_project_repo.update_project.assert_not_called()
        mock_db.commit.assert_not_called()







