import unittest

from overseer.utils.config.config import Config


class TestConfig(unittest.TestCase):

    def test_config_get_parameters(self):
        mock_cfg = {
            'server': {
                'port': 123,
                'debug': True,
                'host': 'localhost'
            }
        }
        cfg = Config()
        cfg.config = mock_cfg

        self.assertEqual(cfg.get('server', 'port'), 123)
        self.assertEqual(cfg.get('server', 'debug'), True),
        self.assertEqual(cfg.get('server', 'host'), 'localhost')
