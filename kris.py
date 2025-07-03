@handle_errors(default_return=True)
def input_year(prompt: str) -> int:
    """
    Prompt user to enter a valid year (integer).
    """
    while True:
        value = input(f"{prompt} (or 0 for back to previous menu): ").strip()
        if value == '0':
            raise UserExit
        try:
            year = int(value)
            logger.info("User entered year: %d for prompt: %s", year, prompt)
            return year
        except ValueError:
            print("Invalid input. Please enter a valid year (numbers only).")


from logger import get_logger

logger = get_logger(__name__)


def handle_errors(default_return=None):
    """
    Универсальный декоратор для логирования и обработки ошибок.

    Аргументы:
        default_return: значение, которое возвращается в случае исключения (если None, пробрасывает дальше)
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} returned successfully")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                if default_return is not None:
                    raise  # если default_return=None — пробрасываем дальше

        return wrapper

    return decorator

import logging

# Configure root logger (do this once in main entry point of the app)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
    ]
)

# Optional: main app logger for generic logs
logger = logging.getLogger("loggi_moviedb")


def get_logger(module_name: str) -> logging.Logger:
    """
    Return a logger instance for the given module name.

    Args:
        module_name (str): The name of the module requesting the logger.

    Returns:
        logging.Logger: Logger instance associated with the module_name.
    """
    return logging.getLogger(module_name)

"""
Logger configuration module.

Sets up basic logging to a file and provides a function to get
module-specific logger instances with consistent formatting and encoding.
"""


import logging

# Configure root logger (do this once in main entry point of the app)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
    ]
)

# Optional: main app logger for generic logs
logger = logging.getLogger("loggi_moviedb")


def get_logger(module_name: str) -> logging.Logger:
    """
    Return a logger instance for the given module name.

    Args:
        module_name (str): The name of the module requesting the logger.

    Returns:
        logging.Logger: Logger instance associated with the module_name.
    """
    return logging.getLogger(module_name)