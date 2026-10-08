from unittest.mock import MagicMock, patch

from src.api import AeroplanesAPI


@patch("src.api.requests.get")
def test_get_request_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"key": "value"}
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    api = AeroplanesAPI()
    result = api.get_request("https://example.com")
    assert result == {"key": "value"}


@patch("src.api.requests.get")
def test_get_request_failure(mock_get):
    import requests
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")

    api = AeroplanesAPI()
    result = api.get_request("https://example.com")
    assert result is None


@patch("src.api.requests.get")
def test_get_country_coordinates_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = [
        {"boundingbox": ["43.0", "51.0", "-10.0", "5.0"]}
    ]
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    api = AeroplanesAPI()
    result = api.get_country_coordinates("Spain")
    assert result == ["43.0", "51.0", "-10.0", "5.0"]


@patch("src.api.requests.get")
def test_get_country_coordinates_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = []
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    api = AeroplanesAPI()
    result = api.get_country_coordinates("NonExistent")
    assert result is None


@patch("src.api.requests.get")
def test_get_aeroplanes_success(mock_get):
    def mock_side_effect(url, params=None, timeout=None):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.raise_for_status = MagicMock()

        if "nominatim" in url:
            mock_resp.json.return_value = [
                {"boundingbox": ["43.0", "51.0", "-10.0", "5.0"]}
            ]
        else:
            mock_resp.json.return_value = {
                "states": [
                    ["abc123", "UAL1621", "United States", 1234567890,
                     None, -3.5, 40.0, 10203.18, False, 268.79, 90.0, None, None, None],
                ]
            }
        return mock_resp

    mock_get.side_effect = mock_side_effect

    api = AeroplanesAPI()
    result = api.get_aeroplanes("Spain")
    assert len(result) == 1
    assert result[0]["callsign"] == "UAL1621"
    assert result[0]["origin_country"] == "United States"
    assert result[0]["velocity"] == 268.79
    assert result[0]["altitude"] == 10203.18


@patch("src.api.requests.get")
def test_get_aeroplanes_no_states(mock_get):
    def mock_side_effect(url, params=None, timeout=None):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.raise_for_status = MagicMock()

        if "nominatim" in url:
            mock_resp.json.return_value = [
                {"boundingbox": ["43.0", "51.0", "-10.0", "5.0"]}
            ]
        else:
            mock_resp.json.return_value = {"states": []}
        return mock_resp

    mock_get.side_effect = mock_side_effect

    api = AeroplanesAPI()
    result = api.get_aeroplanes("Spain")
    assert result == []


@patch("src.api.requests.get")
def test_get_aeroplanes_no_coords(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = []
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    api = AeroplanesAPI()
    result = api.get_aeroplanes("NonExistent")
    assert result == []
