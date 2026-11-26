from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.device_analytics import Analytics
from app.models.devices import DevicesDB
from app.schema.device_analytics_schema import DeviceAnalyticsSchema, DeviceAnalyticsUpdateSchema
from app.repository.devices_repository import DeviceRepository
from app.repository.projects_repository import ProjectRepository
from app.core.exceptions import DeviceNotFoundError
from app.core.exceptions import ProjectNotFoundError
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import get_logger
from uuid import UUID


logger = get_logger(__name__)


class DeviceAnalyticsRepository:

    def __init__(self,db: Session) -> None:
        self._db = db

    def create_analysis(
        self,
        event: DeviceAnalyticsSchema
    ) -> None:
        
        """
        Creating Analysis for a device and storing it in the database
        """
        device_repo = DeviceRepository(db=self._db)

        try:
            device = device_repo.get_device_by_id(
                device_id=event.device_id
            )

            if device is None:
                raise DeviceNotFoundError(f"Device with '{event.device_id}' not found")

            analysis = Analytics(
                device_id = event.device_id,
                total_runtime = event.total_runtime,
                total_kwh = event.total_kwh,
                total_cost = event.total_cost
            )
            self._db.add(analysis)
            self._db.commit()
            self._db.rollback()

        except DeviceNotFoundError as e:
            self._db.rollback()
            logger.warning("Device not found!")
            raise

        except SQLAlchemyError as e:
            self._db.rollback()
            logger.warning("Getting database error")

    def get_analysis_by_id(
        self,
        device_id: UUID
    ) -> Analytics | None:
        """
        Getting device analysis of a single device which is used to show in the dashboard
        """

        query = select(Analytics).where(
            Analytics.device_id == device_id
        )

        analysis = self._db.execute(query).scalar_one_or_none()
        return analysis

    def update_analysis(
        self,
        event: DeviceAnalyticsSchema
    ) -> None:
        """
        Continuous Updation of a device analysis
        """  

        analysis = self.get_analysis_by_id(
            device_id=event.device_id
        )

        if analysis is None:
            analysis = Analytics(
                device_id = event.device_id,
                total_runtime = event.total_runtime,
                total_kwh = event.total_kwh,
                total_cost = event.total_cost
            )
        else:
            analysis.total_runtime += event.total_runtime
            analysis.total_cost += event.total_cost
            analysis.total_kwh += event.total_kwh

        self._db.add(analysis)
        self._db.commit()
        self._db.flush()


    def get_analysis_by_project_id(
        self,
        project_id: UUID
    ) -> dict:
        """
        Retrieves all device usage analysis based on project_id
        (toughest query tbh)
        """
        """
        SQL Query for reference
        SELECT
            d.device_id,
            d.device_name,
            d.status,
            COALESCE(e.total_runtime,0) as total_runtime,
            COALESCE(e.total_kwh,0 ) as total_energy,
            COALESCE(e.total_cost, 0) as total_cost
        FROM devices d LEFT JOIN energy_analysis e on
            d.device_id = e.device_id
        where
            d.project_id = project_id 
        """

        try:
            project_repo = ProjectRepository(db=self._db)
            project = project_repo.get_project_by_id(project_id=project_id)

            if project is None:
                raise ProjectNotFoundError(f"Project with project_id: '{project_id}' not found")
            
            query = (
                select(
                    DevicesDB.device_id,
                    DevicesDB.device_name,
                    DevicesDB.status,
                    func.coalesce(
                        Analytics.total_runtime,0
                    ).label("total_runtime"),
                    func.coalesce(
                        Analytics.total_kwh,0
                    ).label("total_energy"),
                    func.coalesce(
                        Analytics.total_cost,0
                    ).label("total_cost"),
                    Analytics.updated_at
                ).select_from(DevicesDB)
                .outerjoin(
                    Analytics,
                    DevicesDB.device_id == Analytics.device_id
                )
                .where(
                    DevicesDB.project_id == project_id
                )
                .order_by(
                    DevicesDB.device_name
                )
            )

            result = self._db.execute(query).mappings().all()

            return [dict(i) for i in result]

        except ProjectNotFoundError as e:
            logger.warning("Project with project_id: %s not found", project_id)

        except SQLAlchemyError as e:
            logger.exception("Getting Database Error")

        

        
            
