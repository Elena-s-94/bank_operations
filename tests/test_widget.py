import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты функции mask_account_card."""

    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
            ("Счет 73654108430135874319", "Счет **4319"),
            ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
        ],
    )
    def test_mask_various_types(self, input_str, expected):
        assert mask_account_card(input_str) == expected

    def test_card_type_detection(self):
        """Функция распознаёт карту по формату номера (не 'Счет')."""
        result = mask_account_card("Visa 7000792289606361")
        assert "79**" in result
        assert "6361" in result

    def test_account_type_detection(self):
        """Функция распознаёт счёт по слову 'Счет'."""
        result = mask_account_card("Счет 73654108430135874319")
        assert result.startswith("Счет")
        assert "**" in result

    def test_empty_input(self):
        """Пустая строка — IndexError."""
        with pytest.raises(IndexError):
            mask_account_card("")

    def test_invalid_input(self):
        """Некорректные данные — функция не падает."""
        result = mask_account_card("просто текст без номера")
        assert isinstance(result, str)


class TestGetDate:
    """Тесты функции get_date."""

    @pytest.mark.parametrize(
        "date_str, expected",
        [
            ("2024-06-05T14:30:20.72", "05.06.2024"),
            ("2023-12-01T08:15:00.00", "01.12.2023"),
            ("2024-01-15T10:20:05.12", "15.01.2024"),
        ],
    )
    def test_various_dates(self, date_str, expected):
        assert get_date(date_str) == expected

    def test_empty_string(self):
        """Отсутствует дата."""
        result = get_date("")
        assert isinstance(result, str)

    def test_invalid_format(self):
        """Нестандартный формат строки."""
        result = get_date("not-a-date")
        assert isinstance(result, str)
