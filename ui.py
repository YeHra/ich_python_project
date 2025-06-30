#import sys
#sys.path.insert(0, "/home/user1/Документы/ICH/Python/project/lib/python3.12/site-packages")
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
    return input('Введите название фильма или ключевое слово: ')


def category() -> str:
    return input('Введите жанр фильма: ')


def release_year() -> int:
    while True:
        try:
            year = int(input('Введите год выпуска фильма: '))
            # Расширяем диапазон для гибкости
            if 1900 <= year <= 2100:
                return year
            else:
                print('Некорректное значение. Введите год в разумных пределах (например, от 1900 до 2100)')
        except ValueError:
            print('Некорректное значение. Введите целое число для года.')


def start_range_year() -> int:
    while True:
        try:
            year = int(input('Введите начальный год диапазона: '))
            if 1900 <= year <= 2100:
                return year
            else:
                print('Некорректное значение. Введите год в разумных пределах (например, от 1900 до 2100)')
        except ValueError:
            print('Некорректное значение. Введите целое число для года.')


def end_range_year() -> int:
    while True:
        try:
            year = int(input('Введите конечный год диапазона: '))
            if 1900 <= year <= 2100:
                return year
            else:
                print('Некорректное значение. Введите год в разумных пределах (например, от 1900 до 2100)')
        except ValueError:
            print('Некорректное значение. Введите целое число для года.')


# Обновленная функция print_table_data с использованием PrettyTable
def print_table_data(headers: list[str], data: list[tuple]):
    if not data:
        print("Нет данных для отображения.")
        return

    table = PrettyTable()
    table.field_names = headers
    for row in data:
        table.add_row(row)

    print(table)


def ask_for_pagination() -> bool:
    """
    Спрашивает пользователя, хочет ли он вывести следующие 10 результатов.
    Возвращает True, если 'yes', False в противном случае.
    """
    while True:
        ask = input('Вывести следующие 10 результатов? (yes/no): ').lower()
        if ask == 'yes':
            return True
        elif ask == 'no':
            return False
        else:
            print("Некорректный ввод. Пожалуйста, введите 'yes' или 'no'.")