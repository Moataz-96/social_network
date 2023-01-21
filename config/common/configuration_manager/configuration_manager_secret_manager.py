import json
import boto3

from config.common.configuration_manager.configuration_manager_base import \
    ConfigurationManagerBase


class ConfigurationManagerSecretManager(ConfigurationManagerBase):
    def __init__(self):
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=self.region_name)
        secret = client.get_secret_value(SecretId=self.service_name)
        self.secret_dict = json.loads(secret['SecretString'])

    @property
    def sqs_credentials(self):
        return {
            'use_access_credentials': False,
            'access_id': '',
            'access_key': ''
        }

    @property
    def region_name(self):
        return 'eu-west-1'

    @property
    def database_engine(self):
        return self.secret_dict['engine']

    @property
    def database_name(self):
        return self.secret_dict['social_network']

    @property
    def database_host(self):
        return self.secret_dict['host']

    @property
    def database_port(self):
        return self.secret_dict['port']

    @property
    def database_username(self):
        return self.secret_dict['username']

    @property
    def database_password(self):
        return self.secret_dict['password']
