from abc import ABC, abstractmethod
from users.models import CustomUser


class Template(ABC):

    @abstractmethod
    def prepare_template(self, data) -> str:
        return ''

    @abstractmethod
    def send(self, user: CustomUser) -> None:
        return None
