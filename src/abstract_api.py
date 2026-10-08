from abc import ABC, abstractmethod
from typing import Any


class AbstractAPI(ABC):
    """Абстрактный класс для работы с внешними API."""

    @abstractmethod
    def get_request(self, url: str, params: dict | None = None) -> Any:
        """Выполняет GET-запрос к указанному URL с параметрами."""
        pass

    @abstractmethod
    def get_country_coordinates(self, country: str) -> list[str] | None:
        """Возвращает координаты boundingbox страны."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[dict]:
        """Возвращает список самолётов в воздушном пространстве страны."""
        pass
