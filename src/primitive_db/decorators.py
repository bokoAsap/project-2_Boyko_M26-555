# Декораторы, обработчики ошибок, подтверждение, логирование, кеширование
import functools
import prompt


def handle_db_errors(default=None):
    """
    Декоратор для обработки ошибок 
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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
