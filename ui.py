import db
import sys

sys.path.insert(0, "/home/user1/Документы/ICH/Python/project/lib/python3.12/site-packages")
from prettytable import PrettyTable


def show_message(message: str) -> None:
    """
    Принимает сообщение и выводит его пользователю.
    :message: Прописанное в коде сообщение
    """
    print(message)


def main_menu() -> int:
    """
    Функция выводит промт, принимает от пользователя и возвращает пункт меню в виде натурального числа от 0 до 5.
    :return: Число от 0 до 5
    """
    while True:
        prompt = """
            Меню:
            1. Поиск информации о фильме по ключевому слову
            2. Поиск информации о фильме по жанру и году выпуска
            3. Поиск информации о фильме по жанру и диапазону годов выпуска
            4. Вывод пяти самых популярных запросов
            5. Вывод пяти последних запросов
            0. Выход
            Выберите пункт меню (1, 2, 3, 4, 5 или 0):
        """
        try:
            choice = int(input(prompt))
            if 0 <= choice <= 5:
                return choice
            else:
                show_message('Некорректное значение. Введите целое число от 0 до 5')
        except ValueError:
            show_message('Некорректное значение. Введите целое число от 0 до 5')


def keyword() -> str | None:
    """
    Функция принимает от пользователя ключевое слово или его часть
    :return: Строка с ключевым словом или его частью
    """
    user_keyword = input('Введите название фильма или ключевое слово (или 0 для отмены): ').strip()
    if user_keyword == '0':
        return None
    else:
        return user_keyword


def category(db_conn) -> str | None:
    """
    Функция подключается к базе данных, выводит список жанров фильмов, принимает от пользователя жанр, и возвращает
    его, если он есть в списке.
    :db_conn: Подключение к базе данных
    :return: Строка с жанром
    """
    all_categories = [cat[0] for cat in db.all_category(db_conn)]
    lower_all_categories = [cat.lower() for cat in all_categories]
    while True:
        user_category = input('Введите жанр фильма (или 0 для отмены): ').strip().lower()
        if user_category == '0':
            return None
        elif user_category in lower_all_categories:
            return user_category
        show_message('Такого жанра нет в списке. Введите жанр из списка жанров.')


def release_year(db_conn) -> int | None:
    """
    Функция подключается к базе данных, выводит минимальный и максимальный год выпуска фильмов,
    принимает от пользователя год и если он находится в нужном диапазоне, возвращает его.
    :db_conn: Подключение к базе данных
    :return: Год
    """
    min_year = db.min_release_year(db_conn)
    max_year = db.max_release_year(db_conn)
    while True:
        try:
            year = int(input(f'Введите год выпуска ({min_year} - {max_year}) или 0 для отмены: '))
            if year == 0:
                return None
            elif min_year <= year <= max_year:
                return year
            show_message(f'Некорректное значение. Год должен быть в диапазоне {min_year} - {max_year}')
        except ValueError:
            show_message('Некорректное значение. Введите целое число для года')


def start_range_year(db_conn) -> int | None:
    """
    Функция подключается к базе данных, выводит минимальный и максимальный год выпуска фильмов,
    принимает от пользователя год и если он находится в нужном диапазоне, возвращает его.
    :db_conn: Подключение к базе данных
    :return: Год
    """
    min_year = db.min_release_year(db_conn)
    max_year = db.max_release_year(db_conn)
    while True:
        try:
            start_year = int(input(f'Введите начальный год диапазона ({min_year} - {max_year}) или 0 для отмены: '))
            if start_year == 0:
                return None
            if min_year <= start_year <= max_year:
                return start_year
            show_message(f'Некорректное значение. Год должен быть в диапазоне {min_year} - {max_year}')
        except ValueError:
            show_message('Некорректное значение. Введите целое число для года')


def end_range_year(db_conn, start_year: int) -> int | None:
    """
    Функция подключается к базе данных, выводит минимальный и максимальный год выпуска фильмов,
    принимает от пользователя год и если он находится в нужном диапазоне, возвращает его.
    :db_conn: Подключение к базе данных
    :return: Год
    """
    max_year = db.max_release_year(db_conn)
    while True:
        try:
            end_year = int(input(f'Введите конечный год диапазона ({start_year} - {max_year}) или 0 для отмены: '))
            if end_year == 0:
                return None
            elif start_year <= end_year <= max_year:
                return end_year
            else:
                show_message(f'Некорректное значение. Год должен быть в диапазоне {start_year} - {max_year}')
        except ValueError:
            show_message('Некорректное значение. Введите целое число для года')


def print_table_data(headers: list[str], data: list[tuple]) -> None:
    """
    Функция принимает список строк и список кортежей и оформляет их для табличного вывода.
    :param headers: Список заголовков таблицы
    :param data: Список кортежей с данными
    :return: Табличный вывод данных
    """
    if not data:
        show_message("Нет данных для отображения")
        return

    table = PrettyTable()
    table.field_names = headers
    for row in data:
        table.add_row(row)

    print(table)


def ask_for_pagination() -> bool:
    """
    Функция спрашивает пользователя, хочет ли он вывести следующие 10 результатов.
    Возвращает True, если 'yes', False в противном случае.
    :return: True, False
    """
    while True:
        ask = input('Вывести следующие 10 результатов? (yes/no): ').lower()
        if ask == 'yes':
            return True
        elif ask == 'no':
            return False
        else:
            show_message("Некорректный ввод. Пожалуйста, введите 'yes' или 'no'")


def show_error(message: str):
    print(f"Ошибка: {message}")
    return message
