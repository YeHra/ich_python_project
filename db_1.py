import sys
sys.path.insert(0, "/home/user1/Документы/ICH/Python/project/lib/python3.12/site-packages")
import pymysql
import settings


def connection():
    try:
        conn = pymysql.connect(**settings.DATABASE_MYSQL_R) #
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        return None


# db_conn = connection() # Удаляем глобальное подключение


def all_category(db_conn): # Добавлен db_conn параметр
    """
    Функция выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных
    :return: Список кортежей с результатами запроса
    """
    if db_conn is None:
        print("Database connection is not established.")
        return []
    with db_conn.cursor() as cursor:
        cursor.execute('SELECT name FROM category')
        return [row[0] for row in cursor.fetchall()] # Возвращаем список строк, а не кортежей


def min_release_year(db_conn): # Добавлен db_conn параметр
    """
    Функция выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных
    :return: Год
    """
    if db_conn is None:
        print("Database connection is not established.")
        return None
    with db_conn.cursor() as cursor:
        cursor.execute('SELECT MIN(release_year) FROM film')
        result = cursor.fetchone()
        return result[0] if result else None


def max_release_year(db_conn): # Добавлен db_conn параметр
    """
    Функция выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных
    :return: Год
    """
    if db_conn is None:
        print("Database connection is not established.")
        return None
    with db_conn.cursor() as cursor:
        cursor.execute('SELECT MAX(release_year) FROM film')
        result = cursor.fetchone()
        return result[0] if result else None


def search_data_about_film_with_keyword(db_conn, keyword_pattern: str):
    """
    Функция принимает подключение к базе данных, список параметров запроса,
    выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных
    :keyword_pattern: Паттерн,включающий ключевое слово, вводимое пользователем
    :return: Кортеж: (Список кортежей с результатами запроса, Список имен столбцов)
    """
    if db_conn is None:
        print("Database connection is not established.")
        return [], []
    with db_conn.cursor() as cursor:
        query = '''
        SELECT film_id, title, description, release_year, rental_duration, rental_rate, length, replacement_cost, rating
        FROM film 
        WHERE title LIKE %(k_p)s OR description LIKE %(k_p)s
        '''
        cursor.execute(query, {'k_p':keyword_pattern})
        headers = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        return results, headers

# keyword_pattern = f'%{ui.keyword}%' # Удаляем глобальный вызов
# keyword_search_result = search_data_about_film_with_keyword(db_conn, keyword_pattern) # Удаляем глобальный вызов

def search_data_about_film_with_category_year(db_conn, category_year_param: tuple):
    """
    Функция принимает подключение к базе данных, список параметров запроса,
    выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных
    :category_year_param: Кортеж параметров запроса (category_name, release_year)
    :return: Кортеж: (Список кортежей с результатами запроса, Список имен столбцов)
    """
    if db_conn is None:
        print("Database connection is not established.")
        return [], []
    with db_conn.cursor() as cursor:
        query = '''
        SELECT film.film_id, film.title, film.description, film.release_year, category.name AS category_name
        FROM film 
        JOIN film_category ON film.film_id = film_category.film_id 
        JOIN category ON film_category.category_id = category.category_id 
        WHERE (category.name = %s AND film.release_year = %s)
        '''
        cursor.execute(query, category_year_param)
        headers = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        return results, headers

# category_year_param = (ui.category, ui.release_year) # Удаляем глобальный вызов
# category_year_search_result = search_data_about_film_with_category_year(db_conn, category_year_param) # Удаляем глобальный вызов

def search_data_about_film_with_category_range_years(db_conn, category_year_range_param: tuple):
    """
        Функция принимает подключение к базе данных, список параметров запроса,
        выполняет запрос к базе данных и возвращает результат запроса.
        :db_conn: Переменная, которая вызывает подключение к базе данных
        :category_year_range_param: Кортеж параметров запроса (category_name, start_year, end_year)
        :return: Кортеж: (Список кортежей с результатами запроса, Список имен столбцов)
        """
    if db_conn is None:
        print("Database connection is not established.")
        return [], []
    with db_conn.cursor() as cursor:
        query = '''
        SELECT film.film_id, film.title, film.description, film.release_year, category.name AS category_name
        FROM film 
        JOIN film_category ON film.film_id = film_category.film_id 
        JOIN category ON film_category.category_id = category.category_id 
        WHERE (category.name = %s AND film.release_year BETWEEN %s AND %s) 
        '''
        cursor.execute(query, category_year_range_param)
        headers = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        return results, headers

# category_year_range_param = (ui.category(), ui.start_range_year(), ui.end_range_year()) # Удаляем глобальный вызов
# category_year_range_search_result = search_data_about_film_with_category_range_years(db_conn, category_year_range_param) # Удаляем глобальный вызов