import sys
sys.path.insert(0, "/home/user1/Документы/ICH/Python/project/lib/python3.12/site-packages")
import pymysql
import settings
import ui_gem

def connection():
    conn = pymysql.connect(**settings.DATABASE_MYSQL_R)
    return conn


db_conn = connection()
def search_data_about_film_with_category_range_years(db_conn, param):
    with db_conn.cursor() as cursor:
        query = '''SELECT film.*,category.name 
        FROM film JOIN film_category ON film.film_id = film_category.film_id 
        JOIN category ON film_category.category_id = category.category_id 
        WHERE (category.name LIKE %s AND film.release_year BETWEEN %s AND %s) 
        '''
        cursor.execute(query, param)
        return cursor.fetchall()
category_pattern = f'%{category_range_release_year[0]}%'
param = (category_pattern, category_range_release_year[1], category_range_release_year[2])
result = search_data_about_film_with_category_range_years(db_conn, param)

