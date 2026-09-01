from typing import Optional


def get_mask_card_number(card_number: str) -> Optional[str]:
    """Маскирует номер кредитной карты.

    Принимает строку с номером карты, удаляет пробелы и возвращает
    маскированную версию в формате 'XXXX XX** **** XXXX'.

    Args:
        card_number (str): строка с номером кредитной карты.

    Returns:
        Optional[str]: маскированный номер карты, либо None, если номер
        некорректен (не 16 цифр или содержит буквы).
    """
    new_card_number = card_number.replace(" ", "")

    if not new_card_number.isdigit():
        print("Вы ввели неправильный формат номера карты.")
        return None

    if len(new_card_number) != 16:
        print("Номер карты должен содержать 16 цифр.")
        return None

    return f"{new_card_number[:4]} {new_card_number[4:6]}** **** {new_card_number[-4:]}"


def get_mask_account(account_number: str) -> Optional[str]:
    """Маскирует номер банковского счёта.

    Принимает строку с номером счёта, удаляет пробелы и возвращает
    маскированную версию, где видны только последние 4 цифры.

    Args:
        account_number (str): строка с номером счёта.

    Returns:
        Optional[str]: замаскированный номер счёта в формате '**XXXX',
        либо None, если номер некорректен (не 20 цифр или содержит буквы).
    """
    new_account_number = account_number.replace(" ", "")

    if not new_account_number.isdigit():
        print("Вы ввели неправильный формат номера счёта.")
        return None

    if len(new_account_number) != 20:
        print("Номер счёта должен содержать 20 цифр.")
        return None

    return f"**{new_account_number[-4:]}"
