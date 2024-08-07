import unittest
from unittest.mock import patch

from starlette.testclient import TestClient

from app.custom_exceptions.custom_exceptions import NotFoundException
from app.schemas.app import AppResponse
from app.schemas.app_request import AppRequestResponse, AppRequestUpdate
from main import app

client = TestClient(app)


class TestAppRequestsController(unittest.TestCase):

    @patch('app.services.app_request_service.create_app_request')
    def test_create_app_request_success(self, mock_create_app_request):
        app_request_data = {"app_name": "test-2 app", "app_id": 1}
        expected_json_body = {"detail": "App request created successfully"}
        mock_create_app_request.return_value = expected_json_body

        response = client.post("/app_request/create_app_request", json=app_request_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_request_service.create_app_request')
    def test_create_app_request_exception(self, mock_create_app_request):
        mock_create_app_request.side_effect = Exception("Error while creating app request")
        app_request_data = {"app_name": "test-2 app", "app_id": 1}
        expected_json_body = {"detail": "Error while creating app request"}

        response = client.post("app_request/create_app_request", json=app_request_data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_request_service.get_all_app_request')
    def test_get_all_app_request_success(self, mock_get_all_app_request):
        app_request_id = AppResponse(id=1, app_name="test 1 app", app_desc="app desc")
        app_request = AppRequestResponse(id=2, app_name="test app req", app=app_request_id, app_id=1)
        expected_json_body = [
            {"id": 2, "app_name": "test app req", "app_id": 1, "app": {"id": 1, "app_name": "test 1 app", "app_desc": "app desc"}}]
        mock_get_all_app_request.return_value = [app_request]

        response = client.get("app_request/get_all_app_request")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_request_service.get_all_app_request')
    def test_get_all_app_request_exception(self, mock_get_all_app_request):
        mock_get_all_app_request.side_effect = Exception("Error while retrieving all app request")
        expected_json_body = {"detail": "Error while retrieving all app request"}

        response = client.get("app_request/get_all_app_request")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_request_service.delete_app_request')
    def test_delete_app_request_success(self, mock_delete_app_request):
        app_request_id = 1
        mock_delete_app_request.return_value = {"detail": "App request deleted successfully"}

        response = client.delete(f"app_request/delete_app_request?app_request_id={app_request_id}")

        expected_json_body = {"detail": "App request deleted successfully"}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_request_service.delete_app_request')
    def test_delete_app_request_not_found_exception(self, mock_delete_app_request):
        app_request_id = 2
        mock_delete_app_request.side_effect = NotFoundException(app_request_id)
        expected_json_body = {"detail": f"Entry with ID {app_request_id} not found"}

        response = client.delete(f"app_request/delete_app_request?app_request_id={app_request_id}")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_request_service.delete_app_request')
    def test_delete_app_request_exception(self, mock_delete_app_request):
        app_request_id = 2
        mock_delete_app_request.side_effect = Exception("Error while deleting app request")
        expected_json_body = {"detail": f"Error while deleting app request"}

        response = client.delete(f"app_request/delete_app_request?app_request_id={app_request_id}")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_request_service.update_app_request')
    def test_update_app_request_success(self, mock_delete_app_request):
        app_request_id = 1
        mock_delete_app_request.return_value = {"detail": "App request updated successfully"}
        updated_app_request = AppRequestUpdate(app_name="updated app name")

        response = client.put(
            f"/app_request/update_app_request?app_request_id={app_request_id}",
            json=updated_app_request.__dict__
        )
        expected_json_body = {"detail": "App request updated successfully"}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_request_service.update_app_request')
    def test_update_app_request_not_found_exception(self, mock_update_app_request):
        app_request_id = 2
        mock_update_app_request.side_effect = NotFoundException(app_request_id)
        updated_app_request = AppRequestUpdate(app_name="updated app name")

        expected_json_body = {"detail": f"Entry with ID {app_request_id} not found"}

        response = client.put(
            f"/app_request/update_app_request?app_request_id={app_request_id}",
            json=updated_app_request.__dict__
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_request_service.update_app_request')
    def test_update_app_request_exception(self, mock_update_app_request):
        app_request_id = 2
        mock_update_app_request.side_effect = Exception("Error while deleting app request")
        expected_json_body = {"detail": f"Error while updating app request"}
        updated_app_request = AppRequestUpdate(app_name="updated app name")

        response = client.put(
            f"/app_request/update_app_request?app_request_id={app_request_id}",
            json=updated_app_request.__dict__
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), expected_json_body)


if __name__ == '__main__':
    unittest.main()
