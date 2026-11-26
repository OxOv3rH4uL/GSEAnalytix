from fastapi.testclient import TestClient
from app.main import app

class TestProjectDelete:

    def test_delete_project(self):
        project_id = None
        

        with TestClient(app) as client:
            project_name = "Integration Test Project"
            res = client.post(
                "/api/projects",
                json={
                    "project_name": project_name
                }
            )

            data = res.json()["data"]
            project_id = data["project_id"]

            if project_id is not None:
                delete_res = client.delete(
                    f"/api/projects/{project_id}"
                )

            assert delete_res.status_code == 200
            