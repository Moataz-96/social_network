from abc import ABC, abstractmethod


class ConfigurationManagerBase(ABC):

    @property
    def service_name(self) -> str:
        return 'social_network'

    @property
    @abstractmethod
    def region_name(self) -> str:
        return 'eu-west-1'

    @property
    @abstractmethod
    def sqs_credentials(self) -> dict:
        return {}

    @property
    @abstractmethod
    def database_engine(self) -> str:
        return ''

    @property
    @abstractmethod
    def database_name(self) -> str:
        return ''

    @property
    @abstractmethod
    def database_host(self) -> str:
        return ''

    @property
    @abstractmethod
    def database_port(self) -> int:
        return 0

    @property
    @abstractmethod
    def database_username(self) -> str:
        return ''

    @property
    @abstractmethod
    def database_password(self) -> str:
        return ''
