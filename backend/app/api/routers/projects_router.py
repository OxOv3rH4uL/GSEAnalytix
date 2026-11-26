from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.helpers.db import get_db
from uuid import UUID
from app.repository.projects_repository import ProjectRepository
from app.repository.device_analytics_repository import DeviceAnalyticsRepository
from app.services.project_service import ProjectService
from app.schema.api_reponse import APIResponse
from app.core.exceptions_handler import error_response
from app.schema.project_schema import ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse
from app.schema.dashboard_schema import DashboardSchema, ProjectAnalyticsSchema, ProjectDashboardSchema
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
    response_model=APIResponse[ProjectResponse],
    status_code=status.HTTP_201_CREATED
)
def create_project(
    data: ProjectCreateRequest,
    db: Session = Depends(get_db)
) -> APIResponse[ProjectResponse] | JSONResponse:
    
    repo = ProjectRepository(db=db)
    service = ProjectService(db=db, repo=repo)
    try:
        project = service.create_project(data)
        return APIResponse(
            message="Project Created Successfully!",
            data = project
        )
    
    except ProjectFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_409_CONFLICT
        )
    except DatabaseError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@project_router.get(
    "",
    response_model= APIResponse[list[ProjectResponse]],
    status_code = status.HTTP_200_OK
)
def get_all_project(
    db: Session = Depends(get_db)
) -> APIResponse[list[ProjectResponse]] | JSONResponse:
     
    repo = ProjectRepository(db=db)
    service = ProjectService(db=db, repo=repo)
    try:
        projects = service.get_all_projects()
        return APIResponse(
            message="Projects Retrieved Successfully!",
            data=projects
        )
    
    except DatabaseError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

"""
-/api/projects/{project_id} 
Returns all the projects present in the database
Pydantic Validation -> Project Service -> Project Repository -> PostgreSQL
"""

@project_router.get(
    "/{project_id}",
    response_model = APIResponse[ProjectResponse],
    status_code = status.HTTP_200_OK
)
def get_project_by_id(
    project_id: UUID,
    db: Session = Depends(get_db)
) -> APIResponse[ProjectResponse] | JSONResponse:
    
    repo = ProjectRepository(db=db)
    service = ProjectService(db=db, repo=repo)
    try:
        project = service.get_project_by_id(project_id)
        return APIResponse(
            message="Project Retrieved Successfully based on project_id",
            data = project
        )
    
    except ProjectNotFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_404_NOT_FOUND
        )

    except DatabaseError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



"""
- /api/projects/{project_id} 
Updates the project details of a project
Pydantic Validation -> Project Service -> Project Repository -> PostgreSQL
"""

@project_router.put(
    "/{project_id}",
    response_model= APIResponse[ProjectResponse],
    status_code= status.HTTP_200_OK,
) 
def update_project(
    project_id: UUID,
    data: ProjectUpdateRequest,
    db: Session = Depends(get_db),
) -> APIResponse[ProjectResponse] | JSONResponse:
    repo = ProjectRepository(db=db)
    service = ProjectService(db=db, repo=repo)

    try:
        project = service.update_project(project_id=project_id, data=data)
        return APIResponse(
            message = "Project Updated Successfully!",
            data = project
        )

    except ProjectNotFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_404_NOT_FOUND
        )

    except ProjectFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_409_CONFLICT
        )
    
    except DatabaseError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

"""
- /api/project/{project_id}
Deletes the project of project_id
Pydantic Validation -> Project Service -> Project Repository -> PostgreSQL
"""

@project_router.delete(
    "/{project_id}",
    response_model= APIResponse[None],
    status_code = status.HTTP_200_OK  
)

def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db)
) -> APIResponse[None] | JSONResponse:
    
    repo = ProjectRepository(db=db)
    service = ProjectService(db=db, repo=repo)

    try:
        service.delete_project(project_id=project_id)
        return APIResponse(
            message = "Project Deleted Successfully!",
            data = None
        )


    except ProjectNotFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_404_NOT_FOUND
        )

    except DatabaseError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


"""
- GET /api/projects/{project_id}/dashboard
Gets the device analysis for that project
"""
@project_router.get(
    "/{project_id}/dashboard",
    response_model=APIResponse[ProjectDashboardSchema],
    status_code=status.HTTP_200_OK
)
def get_project_dashboard(
    project_id: UUID,
    db: Session = Depends(get_db)
) -> APIResponse[ProjectDashboardSchema]:
    device_analytics_repo = DeviceAnalyticsRepository(db=db)
    project_repo = ProjectRepository(db=db)
    
    try:
        project = project_repo.get_project_by_id(project_id=project_id)

        if project is None:
            raise ProjectFoundError(f"Project with project_id: {project_id} not found")
        result = device_analytics_repo.get_analysis_by_project_id(
            project_id=project_id
        )

        devices = [
            DashboardSchema.model_validate(device)
            for device in result
        ]

        summary = ProjectAnalyticsSchema(
            total_devices= len(devices),
            total_runtime= sum(
                device.total_runtime for device in devices
            ),
            total_energy= sum(
                device.total_energy for device in devices
            ),
            total_cost= sum(
                device.cost for device in devices
            )
        )

        dashboard = ProjectDashboardSchema(
            project_id=project_id,
            project_name= project.project_name,
            summary= summary,
            devices = devices
        )

        return APIResponse(
            message="Project Dashboard Created Successfully!",
            data=dashboard
        )

    except ProjectNotFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    except SQLAlchemyError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
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