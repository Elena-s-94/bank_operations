from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счёта в зависимости от типа входных данных.

    Если в начале строки указано слово «счёт» (регистронезависимо), применяется
    маскировка счёта. В остальных случаях — маскировка номера карты.

    Args:
        info (str): строка вида «Счёт 1234567890123456» или «Карта 1234...».

    Returns:
        str: строка с тем же описанием и замаскированным номером.
    """
    parts = info.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.lower() == "счёт":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Преобразует строку с датой в формат ДД.ММ.ГГГГ.

    Поддерживает входной формат YYYY-MM-DD. Если строка пустая или слишком короткая,
    возвращается пустая строка.

    Args:
        date_str (str): дата в формате «YYYY-MM-DD» (например, «2024-03-11»).

    Returns:
        str: дата в формате «11.03.2024» или пустая строка при некорректных данных.
    """
    if not date_str or len(date_str) < 10:
        return ""

    year = date_str[0:4]
    month = date_str[5:7]
    day = date_str[8:10]

    return f"{day}.{month}.{year}"
