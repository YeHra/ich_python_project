import db
import sys

from db import all_category

sys.path.insert(0, "/home/user1/Документы/ICH/Python/project/lib/python3.12/site-packages")
from prettytable import PrettyTable


def main_menu() -> int:
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
                print('Некорректное значение. Введите целое число от 0 до 5')
        except ValueError:
            print('Некорректное значение. Введите целое число от 0 до 5')


def keyword() -> str:
    user_keyword = input('Введите название фильма или ключевое слово (или 0 для отмены): ').strip()
    if user_keyword == '0':
        return None
    else:
        return user_keyword


def category(db_conn) -> str:
    all_categories = [cat[0] for cat in db.all_category(db_conn)]
    lower_all_categories = [cat.lower() for cat in all_categories]
    while True:
        user_category = input('Введите жанр фильма (или 0 для отмены): ').strip().lower()
        if user_category == '0':
            return None
        elif user_category in lower_all_categories:
            return user_category
        print('Такого жанра нет в списке. Введите жанр из списка жанров.')



def release_year(db_conn) -> int:
    min_year = db.min_release_year(db_conn)
    max_year = db.max_release_year(db_conn)
    while True:
        try:
            year = int(input(f'Введите год выпуска ({min_year} - {max_year}) или 0 для отмены: '))
            if year == 0:
                return None
            elif min_year <= year <= max_year:
                return year
            print(f'Некорректное значение. Год должен быть в диапазоне {min_year} - {max_year}')
        except ValueError:
            print('Некорректное значение. Введите целое число для года')


def start_range_year(db_conn) -> int:
    min_year = db.min_release_year(db_conn)
    max_year = db.max_release_year(db_conn)
    while True:
        try:
            start_year = int(input(f'Введите начальный год диапазона ({min_year} - {max_year}) или 0 для отмены: '))
            if start_year == 0:
                return None
            if min_year <= start_year <= max_year:
                return start_year
            print(f'Некорректное значение. Год должен быть в диапазоне {min_year} - {max_year}')
        except ValueError:
            print('Некорректное значение. Введите целое число для года')


def end_range_year(db_conn, start_year: int) -> int:
    max_year = db.max_release_year(db_conn)
    while True:
        try:
            end_year = int(input(f'Введите конечный год диапазона ({start_year} - {max_year}) или 0 для отмены: '))
            if end_year == 0:
                return None
            elif start_year <= end_year <= max_year:
                return end_year
            else:
                 print(f'Некорректное значение. Год должен быть в диапазоне {start_year} - {max_year}')
        except ValueError:
            print('Некорректное значение. Введите целое число для года')


def print_table_data(headers: list[str], data: list[tuple]):
    if not data:
        print("Нет данных для отображения")
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
    """
    while True:
        ask = input('Вывести следующие 10 результатов? (yes/no): ').lower()
        if ask == 'yes':
            return True
        elif ask == 'no':
            return False
        else:
            print("Некорректный ввод. Пожалуйста, введите 'yes' или 'no'")