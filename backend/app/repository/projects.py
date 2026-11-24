from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.projects import ProjectsDB
from uuid import UUID
from app.core.logger import get_logger

logger = get_logger(__name__)


class ProjectRepository:
    def __init__(self,db: Session) -> None:
        self._db = db


    def create_project(
        self,
        project_name: str
    ) -> ProjectsDB:
        """
        Creating projects and storing it in the database
        """
        logger.debug("Creating project: %s", project_name)

        project = ProjectsDB(project_name=project_name)
        self._db.add(project)
        self._db.flush()
        return project

    def get_all_projects(
        self,
    ) -> list[ProjectsDB]:
        """
        Getting all projects present in the database
        """
        logger.debug("Getting all projects")

        query = select(ProjectsDB).order_by(
            ProjectsDB.created_at.desc()
        )
        projects = list(self._db.scalars(query).all())
        return projects


    def get_project_by_id(
        self,
        project_id: UUID
    ) -> ProjectsDB | None:
        """
        Get a project details by its project_id
        """
        logger.debug("Getting project details for project_id: %s", project_id)

        #We can use db.get too
        query = select(ProjectsDB).where(
            ProjectsDB.project_id == project_id
        )
        project = self._db.execute(query).scalar_one_or_none()
        return project

    def get_project_by_name(
        self,
        project_name: str
    ) -> ProjectsDB | None:
        """
        Get a project details by its project_name
        """
        logger.debug("Getting project details for project_name: %s", project_name)

        query = select(ProjectsDB).where(
            ProjectsDB.project_name == project_name
        )
        project = self._db.execute(query).scalar_one_or_none()
        return project

    def update_project(
        self,
        project_name: str,
        project: ProjectsDB
    ) -> ProjectsDB | None:
        """
        Updating a project details
        """
        logger.debug("Updating project details for project_id: %s", project.project_id)

        project.project_name = project_name
        self._db.flush()

        return project

    def delete_project(
        self,
        project: ProjectsDB
    ) -> None:
        """
        Deleting a project
        """
        logger.debug("Deleting project with project_id: %s", project.project_id)
        self._db.delete(project)
        self._db.flush()
    
    




