from fastapi.testclient import TestClient
from app.main import app

class TestProjectUpdate:

    def test_update_project(self):
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
                create_data = create_res.json()["data"]
                project_id = create_data["project_id"]
                updated_project_name = "Integration Updated Project"

                updated_res = client.put(
                    f"/api/projects/{project_id}",
                    json ={
                        "project_name": updated_project_name
                    }
                )

                assert updated_res.status_code == 200
                data = updated_res.json()["data"]
                up_project_id = data["project_id"]
                assert data["project_name"] == updated_project_name
                assert project_id == up_project_id
        
        finally:
            if project_id is not None:
                client.delete(
                    f"/api/projects/{project_id}"
                )