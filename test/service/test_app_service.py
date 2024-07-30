
import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from app.custom_exceptions.custom_exceptions import NotFoundException
from app.services.app_service import create_app, get_all_apps, delete_app
from app.schemas.app import AppCreate


class TestAppService(unittest.TestCase):

    @patch('app.repositories.app_repository.create_app')
    def test_create_app_success(self, mock_create_app):
        db = MagicMock(spec=Session)
        app_data = {"app_name": "test app", "app_desc": "app description"}
        app_create = AppCreate(**app_data)
        mock_app_instance = MagicMock()
        mock_create_app.return_value = mock_app_instance
        result = create_app(db, app_create)

        mock_create_app.assert_called_once_with(db, app_create)
        self.assertEqual(result, {"detail": "App created successfully"})

    def test_create_app_exception(self):
        db = MagicMock(spec=Session)
        app_data = {"app_name": "test app", "app_desc": "app description"}
        app_create = AppCreate(**app_data)
        db.add.side_effect = Exception("DB Error")
        with self.assertRaises(Exception) as ex:
            create_app(db, app_create)

        db.rollback.assert_called_once()
        self.assertEqual(ex.exception.args[0], "DB Error")

    @patch('app.repositories.app_repository.get_all_apps')
    def test_get_all_apps(self, mock_get_all_apps):
        mocked_app_1 = {"id": 1, "app_name": "test app 1", "app_desc": "app description 1"}
        mocked_app_2 = {"id": 2, "app_name": "test app 2", "app_desc": "app description 2"}
        mocked_apps = [mocked_app_1, mocked_app_2]
        mock_get_all_apps.return_value = mocked_apps
        db = MagicMock()
        result = get_all_apps(db)
        mock_get_all_apps.assert_called_once_with(db)
        self.assertEqual(result, mocked_apps)

    @patch('app.repositories.app_repository.get_app_by_id')
    @patch('app.repositories.app_request_repository.get_app_requests_by_app_id')
    def test_delete_app_success(self, mock_get_app_by_id, mock_get_app_requests_by_app_id):
        mocked_app_1 = {"id": 1, "app_name": "test app 1", "app_desc": "app description 1"}
        mocked_app_request_1 = {"id": 1, "app_name": "test app 1", "app_id": 2}
        mocked_app_request_2 = {"id": 1, "app_name": "test app 1", "app_id": 2}
        associate_app_requests = [mocked_app_request_1, mocked_app_request_2]
        db = MagicMock(spec=Session)
        app_id = 1
        mock_get_app_by_id.return_value = mocked_app_1
        mock_get_app_requests_by_app_id.return_value = associate_app_requests
        result = delete_app(db, app_id)

        mock_get_app_by_id.assert_called_once_with(db, app_id)
        mock_get_app_requests_by_app_id.assert_called_once_with(db, app_id)
        self.assertEqual(result, {"detail": "App and associated app requests deleted successfully"})

    @patch('app.repositories.app_repository.get_app_by_id')
    def test_delete_app_not_found_exception(self, mock_get_app_by_id):
        db = MagicMock(spec=Session)
        app_id = 1
        mock_get_app_by_id.return_value = None
        with self.assertRaises(NotFoundException) as ex:
            delete_app(db, app_id)
        self.assertEqual(ex.exception.message, f"Entry with ID {app_id} not found")

    def test_delete_app_exception(self):
        db = MagicMock(spec=Session)
        app_id = 1
        db.delete.side_effect = Exception("DB Error")
        with self.assertRaises(Exception) as ex:
            delete_app(db, app_id)
        db.rollback.assert_called_once()
        self.assertEqual(ex.exception.args[0], "DB Error")


if __name__ == '__main__':
    unittest.main()
