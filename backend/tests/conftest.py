import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.models.projects import ProjectsDB
from app.models.devices import DevicesDB
from app.repository.projects_repository import ProjectRepository
from app.repository.devices_repository import DeviceRepository
from app.services.project_service import ProjectService
from app.services.device_service import DeviceService



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
def mock_device_repo():
    """
    Mocking/Simulating the Device Repository
    """
    return MagicMock(spec = DeviceRepository)


@pytest.fixture
def project_service(mock_db, mock_project_repo):
    """
    Creating an instance of Project Service using Mock DB and Mock Repo
    -> This unit test is to check Project Service
    """
    return ProjectService(db=mock_db, repo=mock_project_repo)


@pytest.fixture
def device_service(mock_db, mock_project_repo, mock_device_repo):
    """
    Creating an instance of Project Service using Mock DB and Mock Project and Device Repo
    -> This unit test is to check Device Service
    """
    return DeviceService(db=mock_db, project_repo= mock_project_repo, device_repo= mock_device_repo)



@pytest.fixture
def sample_device():
    """
    Example device for Testing
    """

    return DevicesDB(
        device_id = uuid4(),
        project_id = uuid4(),
        device_name="Generator Machine",
        tariff_per_kwh = 20.9
    )
    


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

