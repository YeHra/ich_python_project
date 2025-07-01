import logwriter
import ui
import db


def paginator(headers: list[str], results: list[tuple], page_size: int = 10):
    """
    Выводит результаты по страницам с возможностью продолжения
    :param headers: Заголовки таблицы
    :param results: Список кортежей с данными
    :param page_size: Количество строк на одной странице
    """
    if not results:
        print("По вашему запросу ничего не найдено")
        return

    total_results = len(results)
    current_page = 0

    while True:
        start_index = current_page * page_size
        end_index = start_index + page_size

        page_data = results[start_index:end_index]

        if not page_data:
            print("Все результаты показаны")
            break

        ui.print_table_data(headers, page_data)

        if end_index >= total_results:
            print("Все результаты показаны")
            break

        if not ui.ask_for_pagination():
            break

        current_page += 1


def get_action_result(ans, db_conn):
    """
    Функция принимает от пользователя номер пункта меню и выполняет функции приема данных,
    выполнения запроса к базе данных и запись данных, полученных от пользователя, в словарь
    :ans: Запрос от пользователя
    :db_conn: Подключение к базе данных
    """
    try:
        if ans == 1:
            keyword = ui.keyword()
            if keyword is None:
                return "Возврат в меню", None
            keyword_pattern = f'%{keyword}%'
            results, headers = db.search_data_about_film_with_keyword(db_conn, keyword_pattern)
            logwriter.search_log(search_type = "keyword",
                                 params = {"keyword": keyword},
                                 results_count = len(results))
            return results, headers
        elif ans == 2:
            ui.print_table_data(["Жанр"], db.all_category(db_conn))
            print("Минимальный год выпуска:", db.min_release_year(db_conn))
            print("Максимальный год выпуска:", db.max_release_year(db_conn))
            category = ui.category(db_conn)
            if category is None:
                return "Возврат в меню", None
            release_year = ui.release_year(db_conn)
            if release_year is None:
                return "Возврат в меню", None
            category_year_param = (category, release_year)
            results, headers = db.search_data_about_film_with_category_year(db_conn, category_year_param)
            logwriter.search_log(search_type = "category_year",
                                 params = {"category": category,
                                         "release_year": release_year},
                                 results_count = len(results))
            return results, headers
        elif ans == 3:
            ui.print_table_data(["Жанр"], db.all_category(db_conn))
            print("Минимальный год выпуска:", db.min_release_year(db_conn))
            print("Максимальный год выпуска:", db.max_release_year(db_conn))
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
            logwriter.search_log(search_type = "category_range_year",
                                 params = {"category": category, "min_year": start_year, "max_year": end_year},
                                 results_count = len(results))
            return results, headers
        elif ans == 4:
            results = logwriter.five_popular_query()
            return results, ["Категория", "Количество запросов"]
        elif ans == 5:
            results = logwriter.five_last_query()
            headers = list(results[0].keys())
            data_for_table = [tuple(doc.values()) for doc in results]
            return data_for_table, headers
        elif ans == 0:
            return "Выход по команде пользователя", None
        else:
            return 'Некорректный ввод', None
    except ValueError:
        return 'Некорректный ввод', None
    except Exception as e:
        return f'Произошла ошибка при выполнении запроса: {e}', None


def menu(db_conn):
    while True:
        ans = ui.main_menu()
        if ans == 0:
            message, _ = get_action_result(ans, db_conn)
            print(message)
            break

        result_data, headers = get_action_result(ans, db_conn)

        if result_data == "Возврат в меню":
            continue

        if isinstance(result_data, list):
            if ans in [1, 2, 3]:
                paginator(headers, result_data)
            elif ans in [4, 5]:
                if result_data:
                    ui.print_table_data(headers, result_data)
                else:
                    print("Нет данных для отображения")
        else:
            print(result_data)


def main():
    db_conn = None
    try:
        db_conn = db.connection()
        if db_conn:
            menu(db_conn)
        else:
            print("Не удалось подключиться к базе данных")
    except Exception as error:
        print('Произошла ошибка. ', error)
    finally:
        if db_conn:
            db_conn.close()
            print("Соединение с базой данных закрыто")


if __name__ == '__main__':
    main()