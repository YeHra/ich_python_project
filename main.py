import logwriter
import ui
import db
import settings


def paginator(headers: list[str], results: list[tuple], page_size: int = 10):
    """
    Выводит результаты по страницам с возможностью продолжения.
    :param headers: Заголовки таблицы.
    :param results: Список кортежей с данными.
    :param page_size: Количество строк на одной странице.
    """
    if not results:
        print("По вашему запросу ничего не найдено.")
        return

    total_results = len(results)
    current_page = 0

    while True:
        start_index = current_page * page_size
        end_index = start_index + page_size

        output_data = results[start_index:end_index]

        if not output_data:
            print("Все результаты показаны.")
            break

        print(f"\n--- Результаты ({start_index + 1}-{min(end_index, total_results)} из {total_results}) ---")
        ui.print_table_data(headers, output_data)

        if end_index >= total_results:
            print("Все результаты показаны.")
            break

        if not ui.ask_for_pagination():
            break

        current_page += 1


def get_action_result(ans, db_conn):
    try:
        if ans == 1:
            keyword = ui.keyword()
            keyword_pattern = f'%{keyword}%'
            results, headers = db.search_data_about_film_with_keyword(db_conn, keyword_pattern)
            logwriter.search_log(search_type="keyword", params={"keyword": keyword}, results_count=len(results))
            return results, headers
        elif ans == 2:
            print("Доступные категории:", db.all_category(db_conn))
            print("Минимальный год выпуска:", db.min_release_year(db_conn))
            print("Максимальный год выпуска:", db.max_release_year(db_conn))
            category = ui.category()
            release_year = ui.release_year()
            category_year_param = (category, release_year)
            results, headers = db.search_data_about_film_with_category_year(db_conn, category_year_param)
            logwriter.search_log(search_type="category_year",
                                 params={"category": category, "release_year": release_year},
                                 results_count=len(results))
            return results, headers
        elif ans == 3:
            print("Доступные категории:", db.all_category(db_conn))
            print("Минимальный год выпуска:", db.min_release_year(db_conn))
            print("Максимальный год выпуска:", db.max_release_year(db_conn))
            category = ui.category()
            start_year = ui.start_range_year()
            end_year = ui.end_range_year()
            category_year_range_param = (category, start_year, end_year)
            results, headers = db.search_data_about_film_with_category_range_years(db_conn, category_year_range_param)
            logwriter.search_log(search_type="category_range_year",
                                 params={"category": category, "min_year": start_year, "max_year": end_year},
                                 results_count=len(results))
            return results, headers
        elif ans == 4:
            # logwriter.five_popular_query() уже возвращает форматированные данные
            # headers для этого случая будут "Категория", "Количество запросов"
            results = logwriter.five_popular_query()
            if results:
                # Assuming five_popular_query returns [('Category', count), ...]
                # Headers are fixed for this specific log query
                return results, ["Категория", "Количество запросов"]
            return [], []  # Если нет логов
        elif ans == 5:
            results = logwriter.five_last_query()
            if results:
                # Преобразуем список словарей из logwriter в список кортежей для PrettyTable
                # И динамически получаем заголовки из первого элемента
                headers = list(results[0].keys())
                data_for_table = [tuple(doc.values()) for doc in results]
                return data_for_table, headers
            return [], []
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

        if isinstance(result_data, list):
            # Используем paginator для вывода результатов поиска фильмов (1, 2, 3)
            if ans in [1, 2, 3]:
                paginator(headers, result_data)
            # Для логов (4, 5) просто выводим таблицу, так как там обычно мало записей и пагинация не нужна
            elif ans in [4, 5]:
                if result_data:
                    ui.print_table_data(headers, result_data)
                else:
                    print("Нет данных для отображения.")
        else:
            print(result_data)


def main():
    db_conn = None
    try:
        db_conn = db.connection()
        if db_conn:
            menu(db_conn)
        else:
            print("Не удалось подключиться к базе данных.")
    except Exception as error:
        print('Произошла ошибка. ', error)
    finally:
        if db_conn:
            db_conn.close()
            print("Соединение с базой данных закрыто.")


if __name__ == '__main__':
    main()