import os
from pathlib import Path
from os.path import dirname
from decouple import Config, RepositoryEnv

from config.common.configuration_manager.configuration_manager_base import \
    ConfigurationManagerBase


class ConfigurationManagerEnvFile(ConfigurationManagerBase):
    _BASE_DIR = dirname(Path(__file__).resolve())
    _FILE_NAME = 'local.env'
    _FILE_PATH = os.path.join(_BASE_DIR, 'conf_files', _FILE_NAME)
    config = Config(RepositoryEnv(_FILE_PATH))

    @property
    def sqs_credentials(self):
        return {
            'use_access_credentials': True,
            'access_id': self.config('ACCESS_ID'),
            'access_key': self.config('ACCESS_KEY')
        }

    @property
    def region_name(self):
        return self.config('REGION_NAME')

    @property
    def database_engine(self):
        return self.config('DATABASE_ENGINE')

    @property
    def database_name(self):
        return self.config('DATABASE_NAME')

    @property
    def database_host(self):
        return self.config('DATABASE_HOST')

    @property
    def database_port(self):
        return int(self.config('DATABASE_PORT'))

    @property
    def database_username(self):
        return self.config('DATABASE_USERNAME')

    @property
    def database_password(self):
        return self.config('DATABASE_PASSWORD')
