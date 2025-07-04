import sys
import settings
import ui

sys.path.insert(0, "/home/user1/Документы/ICH/Python/project/lib/python3.12/site-packages")
import pymysql


def connection():
    """
    Функция выполняет подключение к базе данных
    :return: Соединение с базой данных
    """
    try:
        conn = pymysql.connect(**settings.DATABASE_MYSQL_R)  #
        return conn
    except pymysql.Error as e:
        ui.show_message(f'Ошибка подключения: {e}')
        return None


def all_category(db_conn: object) -> list[tuple]:
    """
    Функция выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных
    :return: Список кортежей с результатами запроса
    """
    with db_conn.cursor() as cursor:
        cursor.execute('SELECT DISTINCT name FROM category ORDER BY name')
        categories = [row[0] for row in cursor.fetchall()]
        results = [(category,) for category in categories]
    return results


def min_release_year(db_conn) -> int | None:
    """
    Функция выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных
    :return: Год
    """
    with db_conn.cursor() as cursor:
        cursor.execute('SELECT MIN(release_year) FROM film')
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None


def max_release_year(db_conn) -> int | None:
    """
    Функция выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных
    :return: Год
    """
    with db_conn.cursor() as cursor:
        cursor.execute('SELECT MAX(release_year) FROM film')
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None


def search_data_about_film_with_keyword(db_conn: object, keyword_pattern: str) -> tuple[list, list]:
    """
    Функция принимает подключение к базе данных, список параметров запроса,
    выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных
    :keyword_pattern: Паттерн, включающий ключевое слово, вводимое пользователем
    :return: Кортеж: (Список кортежей с результатами запроса, Список имен столбцов)
    """
    with db_conn.cursor() as cursor:
        query = '''
            SELECT f.film_id, f.title, c.name AS category, f.description, f.release_year,
        (
        SELECT GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ')
        FROM film_actor AS fa
        JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE fa.film_id = f.film_id
        ) AS actors_list, l.name AS language, f.rental_rate, f.length, f.replacement_cost, f.rating    
        FROM film AS f 
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS c ON fc.category_id = c.category_id
        JOIN language as l ON f.language_id = l.language_id 
        WHERE LOWER(f.title) LIKE LOWER(%(k_p)s) OR LOWER(f.description) LIKE LOWER(%(k_p)s)
        '''

        cursor.execute(query, {'k_p': keyword_pattern})
        headers = [col[0] for col in cursor.description]
        results = list(cursor.fetchall())
        return results, headers


def search_data_about_film_with_category_year(db_conn: object, category_year_param: tuple) -> tuple[list, list]:
    """
    Функция принимает подключение к базе данных, список параметров запроса,
    выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных.
    :category_year_param: Кортеж параметров запроса (category_name, release_year)
    :return: Кортеж: (Список кортежей с результатами запроса, Список имен столбцов)
    """
    with db_conn.cursor() as cursor:
        query = '''
            SELECT f.film_id, f.title, c.name AS category, f.description, f.release_year,
        (
        SELECT GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ')
        FROM film_actor AS fa
        JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE fa.film_id = f.film_id
        ) AS actors_list, l.name AS language, f.rental_rate, f.length, f.replacement_cost, f.rating    
        FROM film AS f 
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS c ON fc.category_id = c.category_id
        JOIN language as l ON f.language_id = l.language_id  
        WHERE (LOWER(c.name) = LOWER(%s) AND f.release_year = %s)
        '''
        cursor.execute(query, category_year_param)
        headers = [col[0] for col in cursor.description]
        results = list(cursor.fetchall())
        return results, headers


def search_data_about_film_with_category_range_years(db_conn: object, category_year_range_param: tuple) -> tuple[list, list]:
    """
    Функция принимает подключение к базе данных, список параметров запроса,
    выполняет запрос к базе данных и возвращает результат запроса.
    :db_conn: Переменная, которая вызывает подключение к базе данных.
    :category_year_range_param: Кортеж параметров запроса (category_name, start_year, end_year)
    :return: Кортеж: (Список кортежей с результатами запроса, Список имен столбцов)
    """
    with db_conn.cursor() as cursor:
        query = '''
            SELECT f.film_id, f.title, c.name AS category, f.description, f.release_year,
        (
        SELECT GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ')
        FROM film_actor AS fa
        JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE fa.film_id = f.film_id
        ) AS actors_list, l.name AS language, f.rental_rate, f.length, f.replacement_cost, f.rating    
        FROM film AS f 
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS c ON fc.category_id = c.category_id
        JOIN language as l ON f.language_id = l.language_id 
        WHERE (c.name = %s AND f.release_year BETWEEN %s AND %s) 
        '''
        cursor.execute(query, category_year_range_param)
        headers = [col[0] for col in cursor.description]
        results = list(cursor.fetchall())
        return results, headers
