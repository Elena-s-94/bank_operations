import json
import os

from src.abstract_saver import AbstractSaver
from src.aeroplane import Aeroplane


class JSONSaver(AbstractSaver):
    """Класс для сохранения информации о самолётах в JSON-файл."""

    def __init__(self, file_path: str = "data/aeroplanes.json") -> None:
        self._file_path = file_path
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Создаёт файл и директорию, если их нет."""
        directory = os.path.dirname(self._file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(self._file_path):
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False)

    def _read_all(self) -> list[dict]:
        """Читает все записи из файла."""
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_all(self, data: list[dict]) -> None:
        """Записывает все записи в файл."""
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в JSON-файл."""
        if not isinstance(aeroplane, Aeroplane):
            raise TypeError("Можно добавлять только объекты Aeroplane")
        data = self._read_all()
        aeroplane_dict = aeroplane.to_dict()
        # Проверяем, нет ли уже такого самолёта (по callsign и icao24)
        for item in data:
            if (
                item.get("callsign") == aeroplane_dict["callsign"]
                and item.get("icao24") == aeroplane_dict["icao24"]
            ):
                print(f"Самолёт {aeroplane.callsign} уже существует в файле")
                return
        data.append(aeroplane_dict)
        self._write_all(data)
        print(f"Самолёт {aeroplane.callsign} добавлен в файл")

    def get_aeroplanes_by_criteria(self, **criteria) -> list[Aeroplane]:
        """Получает самолёты из файла по критериям (callsign, origin_country и т.д.)."""
        data = self._read_all()
        result: list[Aeroplane] = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                try:
                    result.append(Aeroplane(
                        callsign=item.get("callsign", "Unknown"),
                        origin_country=item.get("origin_country", "Unknown"),
                        velocity=item.get("velocity", 0.0),
                        altitude=item.get("altitude", 0.0),
                        icao24=item.get("icao24", "Unknown"),
                        longitude=item.get("longitude", 0.0),
                        latitude=item.get("latitude", 0.0),
                    ))
                except (ValueError, TypeError):
                    continue
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт из JSON-файла."""
        if not isinstance(aeroplane, Aeroplane):
            raise TypeError("Можно удалять только объекты Aeroplane")
        data = self._read_all()
        initial_len = len(data)
        data = [
            item
            for item in data
            if not (
                item.get("callsign") == aeroplane.callsign
                and item.get("icao24") == aeroplane.icao24
            )
        ]
        if len(data) < initial_len:
            self._write_all(data)
            print(f"Самолёт {aeroplane.callsign} удалён из файла")
        else:
            print(f"Самолёт {aeroplane.callsign} не найден в файле")

    def get_all(self) -> list[Aeroplane]:
        """Возвращает все самолёты из файла."""
        return self.get_aeroplanes_by_criteria()
