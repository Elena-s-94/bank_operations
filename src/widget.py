from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счета в зависимости
    от типа входных данных."""

    parts = info.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    # проверяем, равно ли значение переменной name строке "счет".
    # Если это так, то вызываем функцию get_mask_account(number)
    # и присваиваем её результат переменной masked_number.
    # В противном случае, вызываем другую функцию,
    # get_mask_card_number(number), и присваиваем её результат
    # masked_number

    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Принимает строку с датой и возвращает корректный
    результат в формате "11.03.2024"."""
    if not date_str or len(date_str) < 10:
        return ""

    year = date_str[0:4]
    month = date_str[5:7]
    day = date_str[8:10]

    return f"{day}.{month}.{year}"
