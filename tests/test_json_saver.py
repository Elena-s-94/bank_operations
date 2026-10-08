import json
import os

import pytest

from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver


@pytest.fixture
def json_saver(tmp_path):
    file_path = os.path.join(str(tmp_path), "test_aeroplanes.json")
    return JSONSaver(file_path)


@pytest.fixture
def sample_aeroplane():
    return Aeroplane("UAL1621", "United States", 268.79, 10203.18, "abc123")


def test_add_aeroplane(json_saver, sample_aeroplane):
    json_saver.add_aeroplane(sample_aeroplane)
    all_planes = json_saver.get_all()
    assert len(all_planes) == 1
    assert all_planes[0].callsign == "UAL1621"


def test_add_duplicate(json_saver, sample_aeroplane):
    json_saver.add_aeroplane(sample_aeroplane)
    json_saver.add_aeroplane(sample_aeroplane)
    all_planes = json_saver.get_all()
    assert len(all_planes) == 1


def test_add_different_aeroplanes(json_saver):
    a1 = Aeroplane("AAA", "Russia", 100.0, 5000.0, "id1")
    a2 = Aeroplane("BBB", "USA", 200.0, 8000.0, "id2")
    json_saver.add_aeroplane(a1)
    json_saver.add_aeroplane(a2)
    all_planes = json_saver.get_all()
    assert len(all_planes) == 2


def test_delete_aeroplane(json_saver, sample_aeroplane):
    json_saver.add_aeroplane(sample_aeroplane)
    json_saver.delete_aeroplane(sample_aeroplane)
    all_planes = json_saver.get_all()
    assert len(all_planes) == 0


def test_delete_not_found(json_saver, sample_aeroplane):
    other = Aeroplane("OTHER", "Canada", 100.0, 5000.0, "other_id")
    json_saver.add_aeroplane(sample_aeroplane)
    json_saver.delete_aeroplane(other)
    all_planes = json_saver.get_all()
    assert len(all_planes) == 1


def test_get_by_criteria_country(json_saver):
    a1 = Aeroplane("AAA", "Russia", 100.0, 5000.0, "id1")
    a2 = Aeroplane("BBB", "USA", 200.0, 8000.0, "id2")
    json_saver.add_aeroplane(a1)
    json_saver.add_aeroplane(a2)
    result = json_saver.get_aeroplanes_by_criteria(origin_country="Russia")
    assert len(result) == 1
    assert result[0].callsign == "AAA"


def test_get_by_criteria_callsign(json_saver, sample_aeroplane):
    json_saver.add_aeroplane(sample_aeroplane)
    result = json_saver.get_aeroplanes_by_criteria(callsign="UAL1621")
    assert len(result) == 1


def test_get_by_criteria_no_match(json_saver, sample_aeroplane):
    json_saver.add_aeroplane(sample_aeroplane)
    result = json_saver.get_aeroplanes_by_criteria(callsign="NOPE")
    assert len(result) == 0


def test_add_non_aeroplane(json_saver):
    with pytest.raises(TypeError):
        json_saver.add_aeroplane("not a plane")


def test_delete_non_aeroplane(json_saver):
    with pytest.raises(TypeError):
        json_saver.delete_aeroplane("not a plane")


def test_ensure_file_created(tmp_path):
    file_path = os.path.join(str(tmp_path), "subdir", "test.json")
    JSONSaver(file_path)
    assert os.path.exists(file_path)


def test_file_valid_json(json_saver, sample_aeroplane):
    json_saver.add_aeroplane(sample_aeroplane)
    with open(json_saver._file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert data[0]["callsign"] == "UAL1621"
