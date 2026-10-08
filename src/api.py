import requests
from typing import Any

from src.abstract_api import AbstractAPI


class AeroplanesAPI(AbstractAPI):
    """Класс для работы с API nominatim и opensky-network."""

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/within"

    def get_request(self, url: str, params: dict | None = None) -> Any:
        """Выполняет GET-запрос к указанному URL."""
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            if "application/json" in response.headers.get("Content-Type", ""):
                return response.json()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def get_country_coordinates(self, country: str) -> list[str] | None:
        """Получает координаты boundingbox страны через nominatim."""
        params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }
        data = self.get_request(self.NOMINATIM_URL, params)
        if not data or not isinstance(data, list) or len(data) == 0:
            print(f"Не удалось найти координаты для страны: {country}")
            return None
        return data[0].get("boundingbox")

    def get_aeroplanes(self, country: str) -> list[dict]:
        """Получает список самолётов в воздушном пространстве страны."""
        bbox = self.get_country_coordinates(country)
        if not bbox or len(bbox) < 4:
            return []

        # bbox возвращает [south, north, west, east] в виде строк
        south, north, west, east = bbox

        params = {
            "lamin": south,
            "lomin": west,
            "lamax": north,
            "lomax": east,
        }

        data = self.get_request(self.OPENSKY_URL, params)
        if not data or not isinstance(data, dict):
            return []

        states = data.get("states", [])
        if not states:
            return []

        aeroplanes = []
        for state in states:
            if not state or len(state) < 10:
                continue
            aeroplane = {
                "callsign": state[1] if state[1] else "Unknown",
                "origin_country": state[2] if state[2] else "Unknown",
                "velocity": round(state[9], 2) if state[9] else 0.0,
                "altitude": round(state[7], 2) if state[7] else 0.0,
                "icao24": state[0] if state[0] else "Unknown",
                "longitude": round(state[5], 2) if state[5] else 0.0,
                "latitude": round(state[6], 2) if state[6] else 0.0,
            }
            aeroplanes.append(aeroplane)

        return aeroplanes
