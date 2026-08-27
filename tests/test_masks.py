import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:
    """Тесты функции get_mask_card_number."""

    def test_standard_card_number(self, sample_card_numbers):
        card = sample_card_numbers[0]
        result = get_mask_card_number(card)
        assert result == "7000 79** **** 6361"

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            ("7000792289606361", "7000 79** **** 6361"),
            ("1234567890123456", "1234 56** **** 3456"),
            ("1111222233334444", "1111 22** **** 4444"),
        ],
    )
    def test_various_card_numbers(self, card_number, expected):
        assert get_mask_card_number(card_number) == expected

    def test_card_with_spaces(self):
        """Номер карты с пробелами внутри."""
        result = get_mask_card_number("7000 7922 8960 6361")
        assert result == "7000 79** **** 6361"

    def test_short_card_number(self):
        """Короткий номер — возвращает None."""
        result = get_mask_card_number("1234")
        assert result is None

    def test_empty_string(self):
        """Пустая строка — возвращает None."""
        result = get_mask_card_number("")
        assert result is None

    def test_non_digit_input(self):
        """Буквы вместо цифр — возвращает None."""
        result = get_mask_card_number("abcd567890123456")
        assert result is None

    def test_long_card_number(self):
        """Слишком длинный номер — возвращает None."""
        result = get_mask_card_number("12345678901234567")
        assert result is None


class TestGetMaskAccount:
    """Тесты функции get_mask_account."""

    def test_standard_account(self, sample_account_numbers):
        account = sample_account_numbers[0]
        result = get_mask_account(account)
        assert result == "**4319"

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("73654108430135874319", "**4319"),
            ("12345678901234567890", "**7890"),
            ("00000000000000000001", "**0001"),
        ],
    )
    def test_various_accounts(self, account_number, expected):
        assert get_mask_account(account_number) == expected

    def test_short_account(self):
        """Счёт короче 20 цифр — возвращает None."""
        result = get_mask_account("12345")
        assert result is None

    def test_empty_account(self):
        """Пустая строка — возвращает None."""
        result = get_mask_account("")
        assert result is None

    def test_non_digit_account(self):
        """Буквы вместо цифр — возвращает None."""
        result = get_mask_account("abcdef12345678901234")
        assert result is None

    def test_long_account(self):
        """Слишком длинный счёт — возвращает None."""
        result = get_mask_account("123456789012345678901")
        assert result is None
