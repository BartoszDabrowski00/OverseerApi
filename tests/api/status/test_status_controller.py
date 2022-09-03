import unittest
from http import HTTPStatus

from overseer.api.status.status_controller import Status


class TestStatusController(unittest.TestCase):
    def test_get_return_value(self):
        status_controller = Status()
        expected_value = {"status": "running"}

        data, status_code, _ = status_controller.get()
        self.assertEqual(data, expected_value)
        self.assertEqual(status_code, HTTPStatus.OK)
