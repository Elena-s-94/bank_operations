from src.masks import get_mask_card_number, get_mask_account

def test_get_mask_card_number_valid():
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number("1111 2222 3333 4444") == "1111 22** **** 4444"

def test_get_mask_card_number_invalid_chars():
    assert get_mask_card_number("1234abcd56789012") is None

def test_get_mask_card_number_wrong_length():
    assert get_mask_card_number("1234567890123") is None      # 13 цифр
    assert get_mask_card_number("12345678901234567") is None  # 17 цифр

def test_get_mask_account_valid():
    acc = "11112222333344445555"
    result = get_mask_account(acc)
    assert result == "**5555"

def test_get_mask_account_invalid_chars():
    assert get_mask_account("1111222233334444555A") is None

def test_get_mask_account_wrong_length():
    assert get_mask_account("1111222233334444555") is None   # 19 цифр
    assert get_mask_account("111122223333444455555") is None # 21 цифра
