from src.aeroplane import Aeroplane


def filter_aeroplanes(
    aeroplanes: list[Aeroplane], filter_words: list[str]
) -> list[Aeroplane]:
    """Фильтрует самолёты по странам регистрации."""
    if not filter_words:
        return aeroplanes
    try:
        result = [
            a for a in aeroplanes
            if any(word.lower() in a.origin_country.lower() for word in filter_words)
        ]
        return result
    except Exception as e:
        print(f"Ошибка при фильтрации: {e}")
        return []


def get_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane], altitude_range: str
) -> list[Aeroplane]:
    """Фильтрует самолёты по диапазону высот. Пример: '1000 - 5000'."""
    if not altitude_range.strip():
        return aeroplanes
    try:
        parts = altitude_range.split("-")
        if len(parts) == 2:
            min_alt = float(parts[0].strip())
            max_alt = float(parts[1].strip())
        elif len(parts) == 1:
            min_alt = float(parts[0].strip())
            max_alt = float("inf")
        else:
            return aeroplanes
        return [a for a in aeroplanes if min_alt <= a.altitude <= max_alt]
    except (ValueError, IndexError) as e:
        print(f"Ошибка при разборе диапазона высот: {e}")
        return aeroplanes


def sort_aeroplanes(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Сортирует самолёты по высоте полёта (по убыванию — DESC)."""
    try:
        return sorted(aeroplanes, key=lambda a: a.altitude, reverse=True)
    except Exception as e:
        print(f"Ошибка при сортировке: {e}")
        return aeroplanes


def get_top_aeroplanes(aeroplanes: list[Aeroplane], n: int) -> list[Aeroplane]:
    """Возвращает топ N самолётов по высоте (после сортировки DESC)."""
    try:
        n = int(n)
        if n <= 0:
            return []
        return aeroplanes[:n]
    except (ValueError, TypeError) as e:
        print(f"Ошибка при получении топ-N: {e}")
        return []


def print_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Выводит список самолётов в консоль в человекочитаемом виде."""
    if not aeroplanes:
        print("Список самолётов пуст")
        return
    print(f"\n{'='*60}")
    print(f"Найдено самолётов: {len(aeroplanes)}")
    print(f"{'='*60}")
    for i, a in enumerate(aeroplanes, 1):
        print(f"{i}. {a}")
    print(f"{'='*60}\n")
