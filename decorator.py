from functools import wraps
import ui


def db_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return None, ui.show_error("Некорректный ввод")
        except Exception as e:
            return None, ui.show_error(f"Ошибка при выполнении запроса: {str(e)}")

    return wrapper
