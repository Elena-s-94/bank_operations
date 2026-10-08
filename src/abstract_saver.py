from abc import ABC, abstractmethod
from src.aeroplane import Aeroplane


class AbstractSaver(ABC):
    """Абстрактный класс для работы с хранилищем данных."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет информацию о самолёте в хранилище."""
        pass

    @abstractmethod
    def get_aeroplanes_by_criteria(self, **criteria) -> list[Aeroplane]:
        """Получает данные из хранилища по указанным критериям."""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет информацию о самолёте из хранилища."""
        pass
