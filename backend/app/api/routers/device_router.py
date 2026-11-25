from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.helpers.db import get_db
from uuid import UUID
from app.repository.projects_repository import ProjectRepository
from app.repository.devices_repository import DeviceRepository
from app.services.device_service import DeviceService
from app.schema.device_schema import DeviceCreateRequest, DeviceUpdateRequest, DeviceResponse
from app.schema.api_reponse import APIResponse
from app.core.exceptions_handler import error_response
from app.core.exceptions import DeviceFoundError, DeviceNotFoundError, DatabaseError, ProjectNotFoundError

device_router = APIRouter(
    prefix="/projects"
)


"""
- POST /api/projects/{project_id}/devices
Creates device for the project
Pydantic Schema Validation -> Device Service(Application Logic and Validation) -> Device Repository(Queries using SQLAlchemy ORM) -> PostgreSQL
"""

@device_router.post(
    "/{project_id}/devices",
    response_model = APIResponse[DeviceResponse],
    status_code = status.HTTP_201_CREATED
)
def create_device(
    project_id: UUID,
    data: DeviceCreateRequest,
    db : Session = Depends(get_db)
) -> APIResponse[DeviceResponse] | JSONResponse:

    project_repo = ProjectRepository(db = db)
    device_repo = DeviceRepository(db=db)
    service = DeviceService(db=db, project_repo=project_repo, device_repo=device_repo)
    
    try:
        device = service.create_device(project_id=project_id, data=data)
        return APIResponse(
            message="Device Created Successfully!",
            data=device
        )

    except ProjectNotFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    except DeviceFoundError as e:
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
- GET - /api/projects/{project_id}/devices
Get all devices based on project_id
"""
@device_router.get(
    "/{project_id}/devices",
    response_model = APIResponse[list[DeviceResponse]],
    status_code = status.HTTP_200_OK
)
def get_all_devices_of_project(
    project_id: UUID,
    db: Session = Depends(get_db)
) -> APIResponse[list[DeviceResponse]] | JSONResponse:
    
    project_repo = ProjectRepository(db = db)
    device_repo = DeviceRepository(db=db)
    service = DeviceService(db=db, project_repo=project_repo, device_repo=device_repo)

    try:
        devices = service.get_devices_by_project_id(project_id=project_id)

        return APIResponse(
            message="Devices Retrieved Successfully!",
            data = devices
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
- GET - /api/projects/{project_id}/devices/{device_id}
Get a device details based on device_id
"""

@device_router.get(
    "/{project_id}/devices/{device_id}",
    response_model = APIResponse[DeviceResponse],
    status_code= status.HTTP_200_OK
)
def get_device_by_id(
    device_id: UUID,
    db: Session = Depends(get_db)
) -> APIResponse[DeviceResponse] | JSONResponse:
    
    project_repo = ProjectRepository(db = db)
    device_repo = DeviceRepository(db=db)
    service = DeviceService(db=db, project_repo=project_repo, device_repo=device_repo)

    try:
        device = service.get_device_by_id(device_id=device_id)
        return APIResponse(
            message="Device Retrieved Successfully based on device_id",
            data = device
        )

    except DeviceNotFoundError as e:
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
- PUT - /api/projects/{project_id}/devices/{device_id}
Updates the device with device_id in project with project_id
"""

@device_router.put(
    "/{project_id}/devices/{device_id}",
    response_model= APIResponse[DeviceResponse],
    status_code=status.HTTP_200_OK
)
def update_device(
    project_id: UUID,
    device_id: UUID,
    data: DeviceUpdateRequest,
    db: Session = Depends(get_db)
) -> APIResponse[DeviceResponse] | JSONResponse:

    project_repo = ProjectRepository(db = db)
    device_repo = DeviceRepository(db=db)
    service = DeviceService(db=db, project_repo=project_repo, device_repo=device_repo)

    try:
        device = service.update_device(project_id=project_id, device_id=device_id,data=data)
        return APIResponse(
            message = "Device Updated Successfully!",
            data = device
        )

        
    except ProjectNotFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    except DeviceFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_409_CONFLICT
        )
    
    except DeviceNotFoundError as e:
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
DELETE - /api/projects/{project_id}/devices/{device_id}
Deletes a device present in a project
"""

@device_router.delete(
    "/{project_id}/devices/{device_id}",
    status_code = status.HTTP_204_NO_CONTENT
)

def delete_device(
    device_id: UUID,
    project_id: UUID,
    db: Session = Depends(get_db)
) -> APIResponse[None] | JSONResponse:
    project_repo = ProjectRepository(db = db)
    device_repo = DeviceRepository(db=db)
    service = DeviceService(db=db, project_repo=project_repo, device_repo=device_repo)

    try:
        service.delete_device(device_id=device_id, project_id=project_id)
        return APIResponse(
            message="Device Deleted Successfully!",
            data=None
        )
    
    except ProjectNotFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    except DeviceNotFoundError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_404_NOT_FOUND
        )

    except DatabaseError as e:
        return error_response(
            e=e,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )