import pytest

from src.aeroplane import Aeroplane


@pytest.fixture
def sample_aeroplane():
    return Aeroplane("UAL1621", "United States", 268.79, 10203.18)


@pytest.fixture
def another_aeroplane():
    return Aeroplane("AAL500", "United States", 200.0, 8000.0)


# --- Тесты инициализации ---

def test_aeroplane_initialization(sample_aeroplane):
    assert sample_aeroplane.callsign == "UAL1621"
    assert sample_aeroplane.origin_country == "United States"
    assert sample_aeroplane.velocity == 268.79
    assert sample_aeroplane.altitude == 10203.18


def test_aeroplane_default_attributes():
    a = Aeroplane("TEST", "Russia", 100.0, 5000.0)
    assert a.icao24 == "Unknown"
    assert a.longitude == 0.0
    assert a.latitude == 0.0


def test_aeroplane_all_attributes():
    a = Aeroplane("TEST", "Russia", 100.0, 5000.0, "abc123", 37.5, 55.7)
    assert a.icao24 == "abc123"
    assert a.longitude == 37.5
    assert a.latitude == 55.7


# --- Тесты валидации ---

def test_invalid_callsign_empty():
    with pytest.raises(ValueError, match="Позывной"):
        Aeroplane("", "Russia", 100.0, 5000.0)


def test_invalid_callsign_none():
    with pytest.raises(ValueError, match="Позывной"):
        Aeroplane(None, "Russia", 100.0, 5000.0)


def test_invalid_country_empty():
    with pytest.raises(ValueError, match="Страна"):
        Aeroplane("TEST", "", 100.0, 5000.0)


def test_invalid_velocity_negative():
    with pytest.raises(ValueError, match="Скорость не может быть отрицательной"):
        Aeroplane("TEST", "Russia", -100.0, 5000.0)


def test_invalid_velocity_string():
    with pytest.raises(ValueError, match="Скорость должна быть числом"):
        Aeroplane("TEST", "Russia", "fast", 5000.0)


def test_invalid_altitude_string():
    with pytest.raises(ValueError, match="Высота должна быть числом"):
        Aeroplane("TEST", "Russia", 100.0, "high")


def test_callsign_stripped():
    a = Aeroplane("  UAL1621  ", "United States", 268.79, 10203.18)
    assert a.callsign == "UAL1621"


def test_country_stripped():
    a = Aeroplane("UAL1621", "  United States  ", 268.79, 10203.18)
    assert a.origin_country == "United States"


# --- Тесты сравнения по скорости ---

def test_eq_same_velocity(sample_aeroplane):
    other = Aeroplane("OTHER", "Canada", 268.79, 5000.0)
    assert sample_aeroplane == other


def test_lt_velocity(sample_aeroplane, another_aeroplane):
    assert another_aeroplane < sample_aeroplane


def test_gt_velocity(sample_aeroplane, another_aeroplane):
    assert sample_aeroplane > another_aeroplane


def test_le_velocity(sample_aeroplane, another_aeroplane):
    assert another_aeroplane <= sample_aeroplane


def test_ge_velocity(sample_aeroplane, another_aeroplane):
    assert sample_aeroplane >= another_aeroplane


def test_compare_with_non_aeroplane(sample_aeroplane):
    assert (sample_aeroplane == 100) is False


# --- Тесты сравнения по высоте ---

def test_compare_altitude_higher(sample_aeroplane, another_aeroplane):
    result = sample_aeroplane.compare_altitude(another_aeroplane)
    assert "выше" in result
    assert "UAL1621" in result


def test_compare_altitude_lower(sample_aeroplane, another_aeroplane):
    result = another_aeroplane.compare_altitude(sample_aeroplane)
    assert "ниже" in result


def test_compare_altitude_equal():
    a1 = Aeroplane("AAA", "Russia", 100.0, 5000.0)
    a2 = Aeroplane("BBB", "Russia", 200.0, 5000.0)
    result = a1.compare_altitude(a2)
    assert "одинаковой высоте" in result


def test_compare_altitude_type_error(sample_aeroplane):
    with pytest.raises(TypeError):
        sample_aeroplane.compare_altitude("not a plane")


# --- Тесты строковых представлений ---

def test_str(sample_aeroplane):
    result = str(sample_aeroplane)
    assert "UAL1621" in result
    assert "United States" in result
    assert "268.79" in result
    assert "10203.18" in result


def test_repr(sample_aeroplane):
    result = repr(sample_aeroplane)
    assert "Aeroplane" in result
    assert "UAL1621" in result
    assert "United States" in result


# --- Тесты to_dict ---

def test_to_dict(sample_aeroplane):
    d = sample_aeroplane.to_dict()
    assert d["callsign"] == "UAL1621"
    assert d["origin_country"] == "United States"
    assert d["velocity"] == 268.79
    assert d["altitude"] == 10203.18
    assert d["icao24"] == "Unknown"


# --- Тесты cast_to_object_list ---

def test_cast_to_object_list():
    data = [
        {"callsign": "AAA", "origin_country": "Russia", "velocity": 100.0, "altitude": 5000.0},
        {"callsign": "BBB", "origin_country": "USA", "velocity": 200.0, "altitude": 8000.0},
    ]
    result = Aeroplane.cast_to_object_list(data)
    assert len(result) == 2
    assert isinstance(result[0], Aeroplane)
    assert result[0].callsign == "AAA"
    assert result[1].callsign == "BBB"


def test_cast_to_object_list_empty():
    result = Aeroplane.cast_to_object_list([])
    assert result == []


def test_cast_to_object_list_invalid_item():
    data = [
        {"callsign": "AAA", "origin_country": "Russia", "velocity": 100.0, "altitude": 5000.0},
        {"callsign": "", "origin_country": "", "velocity": "bad", "altitude": "bad"},
    ]
    result = Aeroplane.cast_to_object_list(data)
    assert len(result) == 1
