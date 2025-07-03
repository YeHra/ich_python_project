import ui
import db
import logwriter


def keyword_search(db_conn: object) -> tuple[str, None] | tuple[list, list]:
    """
    Функция выполняет поиск фильмов по ключевому слову в названии или описании, возвращает результаты
    поиска или сообщение о возврате в меню, записывает запрос в MongoDB.
    :return: Кортеж с результатами
    """
    keyword = ui.keyword()
    if keyword is None:
        return "Возврат в меню", None
    keyword_pattern = f'%{keyword}%'
    results, headers = db.search_data_about_film_with_keyword(db_conn, keyword_pattern)
    logwriter.search_log(search_type="keyword",
                         params={"keyword": keyword},
                         results_count=len(results))
    return results, headers


def category_year_search(db_conn: object) -> tuple[str, None] | tuple[list, list]:
    """
    Функция ищет фильмы по точному совпадению жанра и года выпуска, показывает доступные жанры и
    диапазон годов перед вводом, записывает запрос в MongoDB.
    :return: Кортеж с результатами
    """
    ui.print_table_data(["Жанр"], db.all_category(db_conn))
    ui.print_table_data(["Минимальный год выпуска", "Максимальный год выпуска"],
                        [(db.min_release_year(db_conn), db.max_release_year(db_conn))])
    category = ui.category(db_conn)
    if category is None:
        return "Возврат в меню", None
    release_year = ui.release_year(db_conn)
    if release_year is None:
        return "Возврат в меню", None
    category_year_param = (category, release_year)
    results, headers = db.search_data_about_film_with_category_year(db_conn, category_year_param)
    logwriter.search_log(search_type="category_year",
                         params={"category": category,
                                 "release_year": release_year},
                         results_count=len(results))
    return results, headers


def category_range_year_search(db_conn: object) -> tuple[str, None] | tuple[list, list]:
    """
    Функция ищет фильмы по точному совпадению жанра в диапазоне годов выпуска, показывает доступные жанры и
    диапазон годов перед вводом, записывает запрос в MongoDB.
    :return: Кортеж с результатами
    """
    ui.print_table_data(["Жанр"], db.all_category(db_conn))
    ui.print_table_data(["Минимальный год выпуска", "Максимальный год выпуска"],
                        [(db.min_release_year(db_conn), db.max_release_year(db_conn))])
    category = ui.category(db_conn)
    if category is None:
        return "Возврат в меню", None
    start_year = ui.start_range_year(db_conn)
    if start_year is None:
        return "Возврат в меню", None
    end_year = ui.end_range_year(db_conn, start_year)
    if end_year is None:
        return "Возврат в меню", None
    category_year_range_param = (category, start_year, end_year)
    results, headers = db.search_data_about_film_with_category_range_years(db_conn, category_year_range_param)
    logwriter.search_log(search_type="category_range_year",
                         params={"category": category, "min_year": start_year, "max_year": end_year},
                         results_count=len(results))
    return results, headers


def five_last_search() -> tuple[list[tuple], list]:
    """
    Возвращает 5 последних поисковых запросов из MongoDB
    :return: Кортеж с результатами
    """
    results = logwriter.five_last_query()
    headers = list(results[0].keys())
    data_for_table = [tuple(doc.values()) for doc in results]
    return data_for_table, headers


def five_popular_search() -> tuple[list[tuple], list[str]]:
    """
    Возвращает топ-5 популярных категорий для поиска из MongoDB
    :return: Кортеж с результатами
    """
    results = logwriter.five_popular_query()
    return results, ["Категория", "Количество запросов"]
