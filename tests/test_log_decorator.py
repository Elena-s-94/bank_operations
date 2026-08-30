import pytest

from decorators import log


@pytest.fixture
def temp_log_file(tmp_path):
    return tmp_path / "test.log"


def test_log_success_console(capsys):
    @log()
    def add(x, y):
        return x + y

    result = add(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_error_console(capsys):
    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out


def test_log_to_file(temp_log_file):
    @log(filename=str(temp_log_file))
    def multiply(x, y):
        return x * y

    multiply(3, 4)

    with open(temp_log_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "multiply ok" in content


def test_log_error_to_file(temp_log_file):
    @log(filename=str(temp_log_file))
    def fail():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        fail()

    with open(temp_log_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "fail error: ValueError" in content
