# Декораторы, обработчики ошибок, подтверждение, логирование, кеширование
import functools
import time
from typing import Callable, Hashable, ParamSpec, TypeVar

import prompt

P = ParamSpec("P")
R = TypeVar("R")


def handle_db_errors(
    default: R | None = None
    ) ->  Callable[[Callable[P, R]], Callable[P, R | None]]:
    """
    Декоратор для обработки ошибок 
    """
    def decorator(
        func: Callable[P, R]
        ) -> Callable[P, R | None]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            try:
                return func(*args, **kwargs)
            except FileNotFoundError:
                print("Ошибка: Файл данных не найден. "\
                "Возможно, база данных не инициализирована.")
                return default
            except KeyError as e:
                print(f"Ошибка: Таблица или столбец {e} не найден.")
                return default
            except ValueError as e:
                print(f"Ошибка валидации: {e}")
                return default
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}")
                return default
        return wrapper
    return decorator


def confirm_action(
    action_name: str
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Декоратор для подтверждения выполнения опасных функций
    """
    def decorator(
        func: Callable[P, R]
        ) ->  Callable[P, R | None]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            user_input = prompt.string(
                f'Вы уверены, что хотите выполнить {action_name}? '
                f'[y/n]: '
            )
            if user_input == 'y':
                return func(*args, **kwargs)
            else:
                print('Операция отменена')
                return args[0]
        return wrapper
    return decorator


def log_time(
    func: Callable[P, R]
    ) -> Callable[P, R]:
    """
    Декоратор замеряет время выполнения функции и выводит его в консоль
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        delta = end_time - start_time
        print(f'Функция {func.__name__} выполнилась за {delta:.3f} секунд')
        return result
    return wrapper


def create_cacher() -> Callable[[Hashable, Callable[[], R]], R]:
    """
    Функция с замыканием для кеширования
    """
    cache = {}

    def cache_result(
        key: Hashable,
        value_func: Callable[[], R]
    ) -> R:
        if key not in cache:
            cache[key] = value_func()
        
        return cache[key]

    cache_result.cache_clear = lambda: cache.clear()

    return cache_result
