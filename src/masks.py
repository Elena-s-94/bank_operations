def get_mask_card_number(card_number: str) -> str | None:
    """
    Функция для маскировки номера кредитной карты.

    Функция принимает строку, содержащую номер кредитной карты, и возвращает маскированную версию этого номера.

    Параметры:
    - card_number (str): строка, содержащая номер кредитной карты.

    Возвращает:
    - str: Маскированная строка с номером карты в формате 'XXXX XX** **** XXXX',
      или None, если входные данные некорректны.
    """
    new_card_number = card_number.replace(" ", "")
    if not new_card_number.isdigit():
        print("Вы ввели неправильный формат номера карты.")
        return None
    if len(new_card_number) != 16:
        print("Номер карты не должен содержать больше 16 цифр.")
        return None
    return new_card_number[:4] + " " + new_card_number[4:6] + "** **** " + new_card_number[-4:]


def get_mask_account(account_number: str) -> str | None:
    """
    Функция возвращает замаскированный номер счета, показывающий только последние 4 цифры.
    Она  принимает номер счета в виде строки, удаляет все пробелы и проверяет,
    что он состоит из 20 цифр. Если номер счета не соответствует формату, функция
    выводит сообщение об ошибке и возвращает None. В противном случае возвращает
    строку, где первые 16 цифр заменены на '**'.

    Параметры:
    account_number (str): Номер счета в виде строки.

    Возвращает:
    str: Замаскированный номер счета, если формат корректен, иначе None.
    """
    new_account_number = account_number.replace(" ", "")
    if not new_account_number.isdigit():
        print("Вы ввели неправильный формат номера счета.")
        return None
    if len(new_account_number) != 20:
        print("Номер счета не должен содержать больше 20 цифр.")
        return None
    return f"**{account_number[-4:]}"


if __name__ == "__main__":
    while True:
        input_from_user_account = input("Введите свой номер счета:")
        returned_value = get_mask_account(input_from_user_account)
        if returned_value:
            print(returned_value)
            break

    while True:
        input_from_user = input("Введите свой номер карты:")
        returned_value = get_mask_card_number(input_from_user)
        if returned_value:
            print(returned_value)
            break
