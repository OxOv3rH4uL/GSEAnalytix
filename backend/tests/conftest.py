import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.models.projects import ProjectsDB
from app.repository.projects_repository import ProjectRepository
from app.services.project_service import ProjectService

@pytest.fixture
def mock_db():
    """
    Mocking/Simulating the Database Connection
    """
    return MagicMock(spec=Session)


@pytest.fixture
def mock_project_repo():
    """
    Mocking/Simulating the Project Repository
    """
    return MagicMock(spec = ProjectRepository)

@pytest.fixture
def project_service(mock_db, mock_project_repo):
    """
    Creating an instance of Project Service using Mock DB and Mock Repo
    -> This unit test is to check Project Service
    """
    return ProjectService(db=mock_db, repo=mock_project_repo)


@pytest.fixture
def sample_project():
    """
    Example Project for Testing
    """
    return ProjectsDB(
        project_id = uuid4(),
        project_name = "GSE",
        created_at = datetime.now()
    )

