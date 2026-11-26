from fastapi.testclient import TestClient
from app.main import app

class TestProjectRead:

    def test_get_all_projects(self):
        project_id = None

        try:
        
            with TestClient(app) as client:
                project_name = "Integration Test Project"
                create_res = client.post(
                    "/api/projects",
                    json={
                        "project_name": project_name
                    }
                )

                read_res = client.get(
                    "/api/projects"
                )
                assert read_res.status_code == 200
                data = read_res.json()["data"]
                project_id = data[0]["project_id"]
                assert data[0]["project_name"] == project_name
                assert data[0]["project_id"] is not None

        finally:
            if project_id is not None:
                client.delete(
                    f"/api/projects/{project_id}"
                )