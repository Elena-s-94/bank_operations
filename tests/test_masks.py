from masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_success(caplog):
    card = "1234 5678 9012 3456"
    result = get_mask_card_number(card)
    assert result == "1234 56** **** 3456"
    assert "успешно замаскирован" in caplog.text


def test_get_mask_card_number_wrong_length(caplog):
    card = "1234567890123"  # 13 цифр
    result = get_mask_card_number(card)
    assert result is None
    assert "Некорректная длина номера карты" in caplog.text


def test_get_mask_card_number_non_digit(caplog):
    card = "1234 abcd 9012 3456"
    result = get_mask_card_number(card)
    assert result is None
    assert "Некорректный формат номера карты" in caplog.text


def test_get_mask_account_success(caplog):
    account = "11112222333344445555"
    result = get_mask_account(account)
    assert result == "**5555"
    assert "успешно замаскирован" in caplog.text


def test_get_mask_account_wrong_length(caplog):
    account = "111122223333444455"  # 18 цифр
    result = get_mask_account(account)
    assert result is None
    assert "Некорректная длина номера счёта" in caplog.text


def test_get_mask_account_non_digit(caplog):
    account = "11112222333344445a55"
    result = get_mask_account(account)
    assert result is None
    assert "Некорректный формат номера счёта" in caplog.text
