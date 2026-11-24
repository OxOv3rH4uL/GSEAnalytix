from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.repository.projects_repository import ProjectRepository
from app.schema.project_schema import ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse
from app.core.exceptions import ProjectNotFoundError, DatabaseError, ProjectFoundError
from uuid import UUID
from app.core.logger import get_logger


logger = get_logger(__name__)

class ProjectService:
    """
    Application logic of Project Service
    """

    def __init__(
        self,
        db: Session,
        repo: ProjectRepository
    ) -> None:
        self._db = db
        self._repo = repo


    def create_project(
        self,
        data: ProjectCreateRequest
    ) -> ProjectResponse:
        """
        Creating a project
        """
        try:
            existing_project = self._repo.get_project_by_name(data.project_name)
            if existing_project is not None:
                raise ProjectFoundError(
                    f"Project '{data.project_name}' already exists"
                )

            project = self._repo.create_project(project_name=data.project_name)
            res = ProjectResponse.model_validate(project)
            self._db.commit()

            logger.info("Project created successfully with project_id: %s", res.project_id)
            return res

        except ProjectFoundError:
            logger.warning("Project with project_name: %s already exists", data.project_name)
            self._db.rollback()
            raise
            
            

        except SQLAlchemyError:
            self._db.rollback()
            logger.exception("Getting Database Error")
            raise DatabaseError("Failed to created project")

    def get_all_projects(
        self,
    )-> list[ProjectResponse]:
        """
        Get All Projects
        """

        try:
            projects = self._repo.get_all_projects()
            res = [ProjectResponse.model_validate(project) for project in projects]
            logger.info("Getting all the projects")
            return res
        
        except SQLAlchemyError:
            logger.exception("Getting Database Error")
            self._db.rollback()
            raise DatabaseError("Failed to retrieve project details")

    def get_project_by_id(
        self,
        project_id: UUID
    ) -> ProjectResponse:
        """
        Get project details by its project_id
        """

        try:
            project = self._repo.get_project_by_id(project_id=project_id)

            if project is None:
                logger.warning("Project with project_id: %s is not found", project_id)
                raise ProjectNotFoundError("Project not found")

            res = ProjectResponse.model_validate(project)
            logger.info("Getting project details with project_id: %s", project_id)
            return res    

        except SQLAlchemyError:
            logger.exception("Getting Database Error")
            self._db.rollback()
            raise DatabaseError("Failed to retrieve project details")


    def get_project_by_name(
        self,
        project_name: str
    ) -> ProjectResponse:
        """
        Get a project details by its project_name
        """

        try:
            project = self._repo.get_project_by_name(project_name=project_name)
            if project is None:
                raise ProjectNotFoundError("Project not found")

            
            res = ProjectResponse.model_validate(project)
            logger.info("Getting project details with project_name: %s", project_name)
            return res
                        
        except ProjectNotFoundError:
            logger.warning("Project with project_name: %s is not found", project_name)
            raise
            

        except SQLAlchemyError:
            logger.exception("Getting Database Error")
            self._db.rollback()
            raise DatabaseError("Failed to retrieve project details")

    def update_project(
        self,
        project_id: UUID,
        data: ProjectUpdateRequest
    ) -> ProjectResponse:
        """
        Update project details
        """
        try:
            existing_project = self._repo.get_project_by_id(project_id=project_id)
            if existing_project is None:
                raise ProjectNotFoundError("Project not found")

            project_by_name = self._repo.get_project_by_name(project_name=data.project_name)
            if(project_by_name is not None and project_by_name.project_id != project_id):
                raise ProjectFoundError(f"Project with name '{data.project_name}' already exists")
            
            updated_project = self._repo.update_project(data.project_name,project=existing_project)
            res = ProjectResponse.model_validate(updated_project)
            self._db.commit()

            logger.info("Project with project_id: %s updated successfully!", project_id)
            return res

        except ProjectNotFoundError:
            logger.warning("Project with project_id: %s not found", project_id)
            self._db.rollback()
            raise
            
        
        except ProjectFoundError:
            logger.warning("Project with project_name: %s already exists", data.project_name)
            self._db.rollback()
            raise
            

        except SQLAlchemyError:
            logger.exception("Getting Database Error")
            self._db.rollback()
            raise DatabaseError("Failed to update project details")

    def delete_project(
        self,
        project_id: UUID
    ) -> None:
        """
        Delete a project
        """

        try:
            existing_project = self._repo.get_project_by_id(project_id=project_id)
            if existing_project is None:
                raise ProjectNotFoundError("Project not found")

            self._repo.delete_project(project=existing_project)
            self._db.commit()

            logger.info("Project with project_id: %s deleted successfully!", project_id)

        except ProjectNotFoundError:
            logger.warning("Project with project_id: %s not found", project_id)
            self._db.rollback()
            raise
            

        except SQLAlchemyError:
            logger.exception("Getting Database Error")
            self._db.rollback()
            raise DatabaseError("Failed to delete project details")

