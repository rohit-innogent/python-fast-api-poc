import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.custom_exceptions.custom_exceptions import NotFoundException
from main import app
from app.schemas.app import AppResponse

client = TestClient(app)


class TestAppController(unittest.TestCase):

    @patch('app.services.app_service.create_app')
    def test_create_app_success(self, mock_create_app):
        app_data = {"app_name": "test-2 app", "app_desc": "app description 2"}
        expected_json_body = {"detail": "App created successfully"}
        mock_create_app.return_value = expected_json_body

        response = client.post("/app/create_app", json=app_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_service.create_app')
    def test_create_app_exception(self, mock_create_app):
        mock_create_app.side_effect = Exception("Error while creating app")
        app_data = {"app_name": "test-2 app", "app_desc": "app description 2"}

        response = client.post("app/create_app", json=app_data)

        expected_json_body = {"detail": "Error while creating app"}
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_service.get_all_apps')
    def test_get_all_app_success(self, mock_get_all_apps):
        app_request = AppResponse(id=1, app_name="test 1 app", app_desc="app desc")
        app_res = [app_request]
        expected_json_body = [{"id": 1, "app_name": "test 1 app", "app_desc": "app desc"}]
        mock_get_all_apps.return_value = app_res

        response = client.get("app/get_all_app")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_service.get_all_apps')
    def test_get_all_app_exception(self, mock_get_all_apps):
        mock_get_all_apps.side_effect = Exception("Error while retrieving all apps")
        expected_json_body = {"detail": "Error while retrieving all apps"}

        response = client.get("app/get_all_app")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_service.delete_app')
    def test_delete_app_success(self, mock_delete_app):
        app_id = 1
        mock_delete_app.return_value = {"detail": "App and associated app requests deleted successfully"}
        expected_json_body = {"detail": "App and associated app requests deleted successfully"}

        response = client.delete(f"app/delete_app?app_id={app_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_service.delete_app')
    def test_delete_app_not_found_exception(self, mock_delete_app):
        app_id = 2
        mock_delete_app.side_effect = NotFoundException(app_id)
        expected_json_body = {"detail": f"Entry with ID {app_id} not found"}

        response = client.delete(f"app/delete_app?app_id={app_id}")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), expected_json_body)

    @patch('app.services.app_service.delete_app')
    def test_delete_app_exception(self, mock_delete_app):
        mock_delete_app.side_effect = Exception("Error while deleting app")
        expected_json_body = {"detail": "Error while deleting app"}

        response = client.delete("app/delete_app", params={"app_id": 1})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), expected_json_body)


if __name__ == '__main__':
    unittest.main()
