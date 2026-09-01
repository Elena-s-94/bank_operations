import logging

logger = logging.getLogger("masks")
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str | None:
    """
    Функция для маскировки номера кредитной карты.

    Принимает строку с номером карты, возвращает маскированную версию.
    Формат: 'XXXX XX** **** XXXX'.

    Возвращает None, если входные данные некорректны.
    """
    new_card_number = card_number.replace(" ", "")

    if not new_card_number.isdigit():
        logger.error("Некорректный формат номера карты: '%s' (содержит не только цифры)", card_number)
        return None

    if len(new_card_number) != 16:
        logger.error(
            "Некорректная длина номера карты: '%s' (ожидается 16 цифр, получено %d)",
            card_number,
            len(new_card_number),
        )
        return None

    masked = new_card_number[:4] + " " + new_card_number[4:6] + "** **** " + new_card_number[-4:]
    logger.debug("Номер карты %s успешно замаскирован в %s", card_number, masked)
    return masked


def get_mask_account(account_number: str) -> str | None:
    """
    Возвращает замаскированный номер счёта, показывающий только последние 4 цифры.

    Формат: '**...XXXX' (первые 16 заменены на **, остаются последние 4).

    Возвращает None, если входные данные некорректны.
    """
    new_account_number = account_number.replace(" ", "")

    if not new_account_number.isdigit():
        logger.error("Некорректный формат номера счёта: '%s' (содержит не только цифры)", account_number)
        return None

    if len(new_account_number) != 20:
        logger.error(
            "Некорректная длина номера счёта: '%s' (ожидается 20 цифр, получено %d)",
            account_number,
            len(new_account_number),
        )
        return None

    # Исправляем логику маскирования: показываем последние 4, первые 16 заменяем на **
    masked = "**" + new_account_number[-4:]

    logger.debug("Номер счёта %s успешно замаскирован в %s", account_number, masked)
    return masked
