import functools
import time
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функции.

    Логирует:
      - имя функции и результат при успехе;
      - имя функции, тип ошибки и входные параметры при ошибке.

    Аргументы:
      filename (str, optional): имя файла для записи логов. Если не задано, логи выводятся в консоль.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                duration = end_time - start_time

                message = f"{func_name} ok (took {duration:.6f}s)"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message + "\n")
                else:
                    print(message)

                return result

            except Exception as e:
                end_time = time.perf_counter()
                duration = end_time - start_time
                error_type = type(e).__name__
                message = (
                    f"{func_name} error: {error_type}. "
                    f"Inputs: {args}, {kwargs}. Took {duration:.6f}s"
                )

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message + "\n")
                else:
                    print(message)

                raise

        return wrapper

    return decorator
