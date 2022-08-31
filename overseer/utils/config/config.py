import os

import toml


class Config:
    CONFIG_PATH = os.getenv('OVERSEER_API_CONFIG_PATH', 'config.toml')

    @classmethod
    def __init__(cls):
        cls.config = toml.load(cls.CONFIG_PATH)

    def get(self, section, key):
        return self.config.get(section, {}).get(key, None)


cfg = Config()
