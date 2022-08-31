import unittest

from overseer.api.status.status_controller import Status


class TestStatusController(unittest.TestCase):
    def test_get_return_value(self):
        status_controller = Status()
        expected_value = {"status": "running"}
        self.assertEqual(status_controller.get(), expected_value)  # add assertion here
