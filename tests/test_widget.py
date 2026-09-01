from src.widget import get_date, mask_account_card


def test_get_date_valid():
    # ISO формат с временем: "2019-12-08T22:35:35"
    assert get_date("2019-12-08T22:35:35") == "08.12.2019"


def test_get_date_empty():
    assert get_date("") == ""


def test_get_date_none():
    assert get_date(None) == ""


def test_mask_account_card_card():
    # Строка с картой: последнее слово — номер, остальное — тип/имя
    result = mask_account_card("Visa Platinum 7000792289606361")
    # Ожидается: "Visa Platinum" + результат маскировки карты
    assert result.startswith("Visa Platinum")
    assert "****" in result


def test_mask_account_card_account():
    # Строка со счётом: распознаётся по слову "счет" (регистронезависимо)
    result = mask_account_card("счет 73654108430135874305")
    assert result == "счет **4305"


def test_mask_account_card_account_uppercase():
    # Проверка, что регистр не важен
    result = mask_account_card("СЧЕТ 73654108430135874305")
    assert result == "СЧЕТ **4305"
