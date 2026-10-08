import pytest

from src.aeroplane import Aeroplane
from src.utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    get_top_aeroplanes,
    print_aeroplanes,
    sort_aeroplanes,
)


@pytest.fixture
def sample_aeroplanes():
    return [
        Aeroplane("AAA", "Russia", 100.0, 5000.0),
        Aeroplane("BBB", "United States", 200.0, 8000.0),
        Aeroplane("CCC", "Russia", 300.0, 3000.0),
        Aeroplane("DDD", "Canada", 150.0, 12000.0),
        Aeroplane("EEE", "United States", 250.0, 6000.0),
    ]


# --- Тесты filter_aeroplanes ---

def test_filter_by_country(sample_aeroplanes):
    result = filter_aeroplanes(sample_aeroplanes, ["Russia"])
    assert len(result) == 2
    assert all(a.origin_country == "Russia" for a in result)


def test_filter_by_multiple_countries(sample_aeroplanes):
    result = filter_aeroplanes(sample_aeroplanes, ["Russia", "Canada"])
    assert len(result) == 3


def test_filter_no_match(sample_aeroplanes):
    result = filter_aeroplanes(sample_aeroplanes, ["Germany"])
    assert len(result) == 0


def test_filter_empty_words(sample_aeroplanes):
    result = filter_aeroplanes(sample_aeroplanes, [])
    assert len(result) == 5


def test_filter_case_insensitive(sample_aeroplanes):
    result = filter_aeroplanes(sample_aeroplanes, ["russia"])
    assert len(result) == 2


# --- Тесты get_aeroplanes_by_altitude ---

def test_altitude_range(sample_aeroplanes):
    result = get_aeroplanes_by_altitude(sample_aeroplanes, "4000 - 8000")
    assert len(result) == 3


def test_altitude_single_value(sample_aeroplanes):
    result = get_aeroplanes_by_altitude(sample_aeroplanes, "5000")
    assert all(a.altitude >= 5000 for a in result)


def test_altitude_empty_range(sample_aeroplanes):
    result = get_aeroplanes_by_altitude(sample_aeroplanes, "")
    assert len(result) == 5


def test_altitude_invalid_range(sample_aeroplanes):
    result = get_aeroplanes_by_altitude(sample_aeroplanes, "bad range")
    assert len(result) == 5


# --- Тесты sort_aeroplanes ---

def test_sort_desc_by_altitude(sample_aeroplanes):
    result = sort_aeroplanes(sample_aeroplanes)
    altitudes = [a.altitude for a in result]
    assert altitudes == sorted(altitudes, reverse=True)
    assert result[0].altitude == 12000.0
    assert result[-1].altitude == 3000.0


def test_sort_empty():
    result = sort_aeroplanes([])
    assert result == []


# --- Тесты get_top_aeroplanes ---

def test_top_n(sample_aeroplanes):
    sorted_list = sort_aeroplanes(sample_aeroplanes)
    result = get_top_aeroplanes(sorted_list, 3)
    assert len(result) == 3
    assert result[0].altitude == 12000.0


def test_top_n_more_than_list(sample_aeroplanes):
    sorted_list = sort_aeroplanes(sample_aeroplanes)
    result = get_top_aeroplanes(sorted_list, 10)
    assert len(result) == 5


def test_top_zero(sample_aeroplanes):
    result = get_top_aeroplanes(sample_aeroplanes, 0)
    assert result == []


def test_top_negative(sample_aeroplanes):
    result = get_top_aeroplanes(sample_aeroplanes, -5)
    assert result == []


def test_top_invalid_n(sample_aeroplanes):
    result = get_top_aeroplanes(sample_aeroplanes, "bad")
    assert result == []


# --- Тесты print_aeroplanes ---

def test_print_nonempty(sample_aeroplanes, capsys):
    print_aeroplanes(sample_aeroplanes[:2])
    captured = capsys.readouterr()
    assert "Найдено самолётов: 2" in captured.out
    assert "AAA" in captured.out


def test_print_empty(capsys):
    print_aeroplanes([])
    captured = capsys.readouterr()
    assert "пуст" in captured.out
