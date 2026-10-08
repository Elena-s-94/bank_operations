from src.aeroplane import Aeroplane
from src.api import AeroplanesAPI
from src.json_saver import JSONSaver
from src.utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    get_top_aeroplanes,
    print_aeroplanes,
    sort_aeroplanes,
)


def user_interaction() -> None:
    """Функция взаимодействия с пользователем через консоль."""
    print("=" * 60)
    print("  Добро пожаловать в систему мониторинга самолётов!")
    print("=" * 60)

    # Шаг 1: запрос страны
    country = input("\nВведите название страны (например, Spain): ").strip()
    if not country:
        print("Страна не указана. Выход.")
        return

    print(f"\nЗапрос данных о самолётах над {country}...")
    api = AeroplanesAPI()
    raw_aeroplanes = api.get_aeroplanes(country)

    if not raw_aeroplanes:
        print("Самолёты не найдены или ошибка API. Выход.")
        return

    print(f"Получено записей: {len(raw_aeroplanes)}")

    # Шаг 2: преобразование в объекты
    aeroplanes = Aeroplane.cast_to_object_list(raw_aeroplanes)
    print(f"Объектов самолётов создано: {len(aeroplanes)}")

    # Шаг 3: сохранение в JSON
    json_saver = JSONSaver()
    for a in aeroplanes:
        json_saver.add_aeroplane(a)
    print(f"Самолёты сохранены в файл: {json_saver._file_path}")

    # Шаг 4: топ N по высоте
    try:
        top_n = int(input("\nВведите количество самолётов для топ N: "))
    except ValueError:
        print("Некорректное число. Используем 10.")
        top_n = 10

    sorted_aeroplanes = sort_aeroplanes(aeroplanes)
    top = get_top_aeroplanes(sorted_aeroplanes, top_n)
    print(f"\n--- Топ {top_n} самолётов по высоте ---")
    print_aeroplanes(top)

    # Шаг 5: фильтр по стране регистрации
    filter_input = input(
        "\nВведите страны для фильтрации (через пробел), или Enter для пропуска: "
    ).strip()
    if filter_input:
        filter_words = filter_input.split()
        filtered = filter_aeroplanes(aeroplanes, filter_words)
        print(f"\n--- Самолёты из стран: {', '.join(filter_words)} ---")
        print_aeroplanes(filtered)

    # Шаг 6: фильтр по диапазону высот
    altitude_input = input(
        "\nВведите диапазон высот (например, '1000 - 5000'), или Enter для пропуска: "
    ).strip()
    if altitude_input:
        ranged = get_aeroplanes_by_altitude(aeroplanes, altitude_input)
        ranged_sorted = sort_aeroplanes(ranged)
        print(f"\n--- Самолёты в диапазоне высот: {altitude_input} ---")
        print_aeroplanes(ranged_sorted)

    print("\nРабота завершена. Спасибо!")


if __name__ == "__main__":
    user_interaction()
