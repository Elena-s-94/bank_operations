from src.widget import mask_account_card, get_date

def test_mask_account_card_account():
    assert mask_account_card("счет 11112222333344445555") == "счет **5555"

def test_mask_account_card_card():
    assert mask_account_card("карта 1234567890123456") == "карта 1234 56** **** 3456"

def test_get_date_basic():
    assert get_date("2024-03-11") == "11.03.2024"
