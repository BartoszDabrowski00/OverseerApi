import os

import toml


class Config:
    CONFIG_PATH = os.getenv('OVERSEER_API_CONFIG_PATH', 'config.toml')
    config = None

    @classmethod
    def get(cls, section, key):
        if cls.config is None:
            cls.config = toml.load(cls.CONFIG_PATH)

        return cls.config.get(section, {}).get(key, None)
