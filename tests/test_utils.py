import json

from src.utils import read_json_file


def test_read_json_file_success(tmp_path):
    file_path = tmp_path / "operations.json"
    data = [{"id": 1, "state": "EXECUTED"}]
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = read_json_file(str(file_path))
    assert result == data


def test_read_json_file_not_found():
    result = read_json_file("nonexistent_file.json")
    assert result == []


def test_read_json_file_empty_file(tmp_path):
    file_path = tmp_path / "empty.json"
    file_path.write_text("", encoding="utf-8")

    result = read_json_file(str(file_path))
    assert result == []


def test_read_json_file_not_a_list(tmp_path):
    file_path = tmp_path / "dict.json"
    file_path.write_text(json.dumps({"key": "value"}), encoding="utf-8")

    result = read_json_file(str(file_path))
    assert result == []
