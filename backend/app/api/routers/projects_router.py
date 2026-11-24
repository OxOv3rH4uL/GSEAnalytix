from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from app.helpers.db import get_db
from uuid import UUID
from app.repository.projects_repository import ProjectRepository
from app.services.project_service import ProjectService
from app.schema.project_schema import ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse
from app.core.exceptions import ProjectFoundError, ProjectNotFoundError, DatabaseError

project_router = APIRouter(
    prefix="/projects"
)


"""
Project Creation Route
- /api/projects 
Pydantic validates the request and sends to the service
Service validates few conditions and communicates with DB via Repository
If it is successful, DB is committed

Pydantic Validation -> Project Service -> Project Repository -> PostgreSQL
"""

@project_router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    data: ProjectCreateRequest,
    db: Session = Depends(get_db)
) -> ProjectResponse:
    
    repo = ProjectRepository(db=db)
    service = ProjectService(db=db, repo=repo)
    try:
        return service.create_project(data)
    
    except ProjectFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            details=str(e)
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=str(e)
        )


@project_router.get(
    "",
    response_model= list[ProjectResponse],
    status_code = status.HTTP_200_OK
)
def get_all_project(
    db: Session = Depends(get_db)
) -> list[ProjectResponse]:
     
    repo = ProjectRepository(db=db)
    service = ProjectService(db=db, repo=repo)
    try:
        return service.get_all_projects()
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=str(e)
        )

"""
-/api/projects/{project_id} 
Returns all the projects present in the database
Pydantic Validation -> Project Service -> Project Repository -> PostgreSQL
"""

@project_router.get(
    "/{project_id}",
    status_code = status.HTTP_200_OK
)
def get_project_by_id(
    project_id: UUID,
    db: Session = Depends(get_db)
) -> ProjectResponse:
    
    repo = ProjectRepository(db=db)
    service = ProjectService(db=db, repo=repo)
    try:
        return service.get_project_by_id(project_id)
    
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details = str(e)
        )

    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=str(e)
        )



"""
- /api/projects/{project_id} 
Updates the project details of a project
Pydantic Validation -> Project Service -> Project Repository -> PostgreSQL
"""

@project_router.put(
    "/{project_id}",
    status_code= status.HTTP_200_OK,
) 
def update_project(
    project_id: UUID,
    data: ProjectUpdateRequest,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    repo = ProjectRepository(db=db)
    service = ProjectService(db=db, repo=repo)

    try:
        return service.update_project(project_id=project_id, data=data)

    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details = str(e)
        )

    except ProjectFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            details = str(e)
        )
    
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=str(e)
        )

"""
- /api/project/{project_id}
Deletes the project of project_id
Pydantic Validation -> Project Service -> Project Repository -> PostgreSQL
"""

@project_router.delete(
    "/{project_id}",
    status_code = status.HTTP_204_NO_CONTENT
)

def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db)
) -> None:
    
    repo = ProjectRepository(db=db)
    service = ProjectService(db=db, repo=repo)

    try:
        return service.delete_project(project_id=project_id)


    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details = str(e)
        )

    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=str(e)
        )



# """
# - /api/projects/{project_name} 
# Returns the project details of the project_name
# Pydantic Validation -> Project Service -> Project Repository -> PostgreSQL
# """

# @project_router.get(
#     "/{project_name}",
#     status_code = status.HTTP_200_OK
# )

# def get_project_by_name(
#     project_name: str,
#     db: Session = Depends(get_db)
# ) -> ProjectResponse:
    
#     repo = ProjectRepository(db=db)
#     service = ProjectService(db=db, repo=repo)
#     try:
#         service.get_project_by_name(project_name)
    
#     except ProjectNotFoundError as e:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail = str(e)
#         )

#     except DatabaseError as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             details=str(e)
#         )