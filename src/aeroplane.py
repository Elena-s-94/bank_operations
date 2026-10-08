from typing import Any


class Aeroplane:
    """Класс для описания самолёта с валидацией и сравнением."""

    def __init__(
        self,
        callsign: str,
        origin_country: str,
        velocity: float,
        altitude: float,
        icao24: str = "Unknown",
        longitude: float = 0.0,
        latitude: float = 0.0,
    ) -> None:
        self._callsign = self._validate_callsign(callsign)
        self._origin_country = self._validate_country(origin_country)
        self._velocity = self._validate_velocity(velocity)
        self._altitude = self._validate_altitude(altitude)
        self._icao24 = icao24 if icao24 else "Unknown"
        self._longitude = float(longitude) if longitude else 0.0
        self._latitude = float(latitude) if latitude else 0.0

    # --- Валидация ---

    @staticmethod
    def _validate_callsign(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Позывной должен быть непустой строкой")
        return value.strip()

    @staticmethod
    def _validate_country(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Страна должна быть непустой строкой")
        return value.strip()

    @staticmethod
    def _validate_velocity(value: float) -> float:
        try:
            v = float(value)
        except (TypeError, ValueError):
            raise ValueError("Скорость должна быть числом")
        if v < 0:
            raise ValueError("Скорость не может быть отрицательной")
        return v

    @staticmethod
    def _validate_altitude(value: float) -> float:
        try:
            a = float(value)
        except (TypeError, ValueError):
            raise ValueError("Высота должна быть числом")
        return a

    # --- Свойства ---

    @property
    def callsign(self) -> str:
        return self._callsign

    @property
    def origin_country(self) -> str:
        return self._origin_country

    @property
    def velocity(self) -> float:
        return self._velocity

    @property
    def altitude(self) -> float:
        return self._altitude

    @property
    def icao24(self) -> str:
        return self._icao24

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def latitude(self) -> float:
        return self._latitude

    # --- Сравнение по скорости ---

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._velocity == other._velocity

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._velocity < other._velocity

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._velocity <= other._velocity

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._velocity > other._velocity

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._velocity >= other._velocity

    # --- Сравнение по высоте ---

    def compare_altitude(self, other: "Aeroplane") -> str:
        """Сравнивает два самолёта по высоте полёта."""
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только объекты Aeroplane")
        if self._altitude > other._altitude:
            return f"{self._callsign} выше {other._callsign}"
        if self._altitude < other._altitude:
            return f"{self._callsign} ниже {other._callsign}"
        return f"{self._callsign} и {other._callsign} на одинаковой высоте"

    # --- Строковые представления ---

    def __str__(self) -> str:
        return (
            f"Самолёт: {self._callsign}, страна: {self._origin_country}, "
            f"скорость: {self._velocity} м/с, высота: {self._altitude} м"
        )

    def __repr__(self) -> str:
        return (
            f"Aeroplane(callsign={self._callsign!r}, "
            f"origin_country={self._origin_country!r}, "
            f"velocity={self._velocity}, altitude={self._altitude})"
        )

    # --- Преобразование ---

    @staticmethod
    def cast_to_object_list(data: list[dict]) -> list["Aeroplane"]:
        """Преобразует список словарей в список объектов Aeroplane."""
        result: list[Aeroplane] = []
        for item in data:
            try:
                aeroplane = Aeroplane(
                    callsign=item.get("callsign", "Unknown"),
                    origin_country=item.get("origin_country", "Unknown"),
                    velocity=item.get("velocity", 0.0),
                    altitude=item.get("altitude", 0.0),
                    icao24=item.get("icao24", "Unknown"),
                    longitude=item.get("longitude", 0.0),
                    latitude=item.get("latitude", 0.0),
                )
                result.append(aeroplane)
            except (ValueError, TypeError) as e:
                print(f"Ошибка при создании объекта самолёта: {e}")
        return result

    def to_dict(self) -> dict:
        """Возвращает словарь с данными самолёта."""
        return {
            "callsign": self._callsign,
            "origin_country": self._origin_country,
            "velocity": self._velocity,
            "altitude": self._altitude,
            "icao24": self._icao24,
            "longitude": self._longitude,
            "latitude": self._latitude,
        }
