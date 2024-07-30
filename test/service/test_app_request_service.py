import unittest
from unittest.mock import patch, MagicMock

from sqlalchemy.orm import Session

from app.custom_exceptions.custom_exceptions import NotFoundException
from app.models import AppRequest
from app.schemas.app_request import AppRequestCreate, AppRequestUpdate
from app.services.app_request_service import create_app_request, get_all_app_request, delete_app_request, \
    update_app_request


class TestAppService(unittest.TestCase):

    @patch('app.repositories.app_request_repository.create_app_request')
    def test_create_app_success(self, mock_create_app_request):
        db = MagicMock(spec=Session)
        app_request_data = {"app_name": "test app", "app_id": 1}
        app_request_create = AppRequestCreate(**app_request_data)
        mock_app_instance = MagicMock()
        mock_create_app_request.return_value = mock_app_instance

        result = create_app_request(db, app_request_create)

        mock_create_app_request.assert_called_once_with(db, app_request_create)
        self.assertEqual(result, {"detail": "App request created successfully"})

    def test_create_app_request_exception(self):
        db = MagicMock(spec=Session)
        app_request_data = {"app_name": "test app", "app_id": 1}
        app_request_create = AppRequestCreate(**app_request_data)
        db.add.side_effect = Exception("DB Error")
        with self.assertRaises(Exception) as ex:
            create_app_request(db, app_request_create)

        db.rollback.assert_called_once()
        self.assertEqual(ex.exception.args[0], "DB Error")

    @patch('app.repositories.app_request_repository.get_all_app_request')
    def test_get_all_app_request(self, mock_get_all_app_request):
        mocked_app_request_1 = {"id": 1, "app_name": "test app 1", "app_id": 2, "app": None}
        mocked_app_request_2 = {"id": 1, "app_name": "test app 1", "app_id": 2, "app": None}
        mocked_app_request_list = [mocked_app_request_1, mocked_app_request_2]
        mock_get_all_app_request.return_value = mocked_app_request_list
        db = MagicMock()

        result = get_all_app_request(db)

        mock_get_all_app_request.assert_called_once_with(db)
        self.assertEqual(result, mocked_app_request_list)

    @patch('app.repositories.app_request_repository.get_app_request_by_id')
    def test_delete_app_request_success(self, mock_get_app_request_by_id):
        app_request_id = 2
        mocked_app_request_1 = {"id": 1, "app_name": "test app 1", "app_id": 2}
        db = MagicMock(spec=Session)
        mock_get_app_request_by_id.return_value = mocked_app_request_1

        result = delete_app_request(db, app_request_id)

        mock_get_app_request_by_id.assert_called_once_with(db, app_request_id)
        self.assertEqual(result, {"detail": "App request deleted successfully"})

    @patch('app.repositories.app_request_repository.get_app_request_by_id')
    def test_delete_app_reqeust_not_found_exception(self, mock_get_app_request_by_id):
        db = MagicMock(spec=Session)
        app_request_id = 2
        mock_get_app_request_by_id.return_value = None
        with self.assertRaises(NotFoundException) as ex:
            delete_app_request(db, app_request_id)
        self.assertEqual(ex.exception.message, f"Entry with ID {app_request_id} not found")

    def test_delete_app_request_exception(self):
        db = MagicMock(spec=Session)
        app_request_id = 1
        db.delete.side_effect = Exception("DB Error")
        with self.assertRaises(Exception) as ex:
            delete_app_request(db, app_request_id)
        db.rollback.assert_called_once()
        self.assertEqual(ex.exception.args[0], "DB Error")

    @patch('app.repositories.app_request_repository.get_app_request_by_id')
    def test_update_app_request_success(self, mock_get_app_request_by_id):
        app_request_id = 2
        db = MagicMock(spec=Session)
        mock_app_request = AppRequest(id=1, app_name="test app", app_id=2, app=None)
        mock_get_app_request_by_id.return_value = mock_app_request
        updated_app_request = AppRequestUpdate(app_name="updated app name")

        result = update_app_request(db, app_request_id, updated_app_request)

        mock_get_app_request_by_id.assert_called_once_with(db, app_request_id)
        db.commit.assert_called_once()
        self.assertEqual(result, {"detail": "App request updated successfully"})

    @patch('app.repositories.app_request_repository.get_app_request_by_id')
    def test_update_app_reqeust_not_found_exception(self, mock_get_app_request_by_id):
        db = MagicMock(spec=Session)
        app_request_id = 2
        updated_app_request = AppRequestUpdate(app_name="updated app name")
        mock_get_app_request_by_id.return_value = None
        with self.assertRaises(NotFoundException) as ex:
            update_app_request(db, app_request_id, updated_app_request)
        self.assertEqual(ex.exception.message, f"Entry with ID {app_request_id} not found")

    def test_update_app_request_exception(self):
        db = MagicMock(spec=Session)
        app_request_id = 1
        db.commit.side_effect = Exception("DB Error")
        updated_app_request = AppRequestUpdate(app_name="updated app name")
        with self.assertRaises(Exception) as ex:
            update_app_request(db, app_request_id, updated_app_request)
        db.rollback.assert_called_once()
        self.assertEqual(ex.exception.args[0], "DB Error")


if __name__ == '__main__':
    unittest.main()