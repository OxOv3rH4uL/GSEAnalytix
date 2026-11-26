from fastapi.testclient import TestClient
from app.main import app

class TestProjectCreate:

    def test_create_project(self):
        project_id = None

        try:

            with TestClient(app) as client:
                project_name = "Integration Test Project"
                res = client.post(
                    "/api/projects",
                    json={
                        "project_name": project_name
                    }
                )

                assert res.status_code == 201

                data = res.json()["data"]
                project_id = data["project_id"]
                assert data["project_name"] == project_name
                assert data["project_id"] is not None

        finally:
            if project_id is not None:
                client.delete(
                    f"/api/projects/{project_id}"
                )
        