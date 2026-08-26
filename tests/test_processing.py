import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты функции filter_by_state."""

    @pytest.mark.parametrize(
        "state, expected_count",
        [
            ("EXECUTED", 2),
            ("CANCELED", 2),
        ],
    )
    def test_filter_by_state(self, sample_dict_list, state, expected_count):
        result = filter_by_state(sample_dict_list, state)
        assert len(result) == expected_count
        assert all(item["state"] == state for item in result)

    def test_default_state(self, sample_dict_list):
        """По умолчанию state='EXECUTED'."""
        result = filter_by_state(sample_dict_list)
        assert all(item["state"] == "EXECUTED" for item in result)

    def test_nonexistent_state(self, sample_dict_list):
        """Статус, которого нет в списке."""
        result = filter_by_state(sample_dict_list, "PENDING")
        assert result == []

    def test_empty_list(self):
        """Пустой список."""
        result = filter_by_state([], "EXECUTED")
        assert result == []


class TestSortByDate:
    """Тесты функции sort_by_date."""

    def test_sort_descending(self, sample_dict_list):
        """Сортировка по убыванию (по умолчанию)."""
        result = sort_by_date(sample_dict_list)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)

    def test_sort_ascending(self, sample_dict_list):
        """Сортировка по возрастанию — sorted_order=False."""
        result = sort_by_date(sample_dict_list, sorted_order=False)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates)

    def test_same_dates(self, same_date_list):
        """Одинаковые даты — порядок сохраняется."""
        result = sort_by_date(same_date_list)
        assert len(result) == 3
        assert all(item["date"] == "2024-01-01T00:00:00.00" for item in result)

    def test_empty_list(self):
        """Пустой список."""
        result = sort_by_date([])
        assert result == []

    def test_single_item(self):
        """Один элемент в списке."""
        data = [{"id": 1, "state": "EXECUTED", "date": "2024-01-01T00:00:00.00"}]
        result = sort_by_date(data)
        assert len(result) == 1
        assert result[0]["id"] == 1
