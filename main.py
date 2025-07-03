import ui
import db
import search_result


def paginator(headers: list[str], results: list[tuple], page_size: int = 10) -> None:
    """
    Функция выводит результаты по страницам с возможностью продолжения.
    :headers: Заголовки таблицы.
    :results: Список кортежей с данными.
    :page_size: Количество строк на одной странице.
    """
    if not results:
        ui.show_message("По вашему запросу ничего не найдено")
        return

    total_results = len(results)
    current_page = 0

    while True:
        start_index = current_page * page_size
        end_index = start_index + page_size

        page_data = results[start_index:end_index]

        if not page_data:
            ui.show_message("Все результаты показаны")
            break

        ui.print_table_data(headers, page_data)

        if end_index >= total_results:
            ui.show_message("Все результаты показаны")
            break

        if not ui.ask_for_pagination():
            break

        current_page += 1


def get_action_result(ans: object, db_conn: object) -> tuple | None:
    """
    Функция обрабатывает пользовательский выбор из меню и выполняет соответствующие действия с БД.
    :ans: Запрос от пользователя.
    :db_conn: Подключение к базе данных
    :return: Кортеж различных объектов
    """
    try:
        if ans == 1:
            return search_result.keyword_search(db_conn)
        elif ans == 2:
            return search_result.category_year_search(db_conn)
        elif ans == 3:
            return search_result.category_range_year_search(db_conn)
        elif ans == 4:
            return search_result.five_popular_search()
        elif ans == 5:
            return search_result.five_popular_search()
        elif ans == 0:
            return ui.show_message('Выход по команде пользователя'), None
        else:
            return ui.show_message('Некорректный ввод'), None
    except ValueError:
        return ui.show_message('Некорректный ввод'), None
    except Exception as e:
        return ui.show_message(f'Произошла ошибка при выполнении запроса: {e}'), None


def menu(db_conn: object) -> None:
    """
    Функция обрабатывает выбор пунктов меню и отображает результаты.
    :db_conn: Подключение к базе данных
    """
    while True:
        ans = ui.main_menu()
        if ans == 0:
            ui.show_message('Выход из программы')
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
                    ui.show_message("Нет данных для отображения")


def main() -> None:
    """
    Функция входа в приложение. Управляет подключением к БД и запускает главное меню приложения
    """
    db_conn = None
    try:
        db_conn = db.connection()
        if db_conn:
            menu(db_conn)
        else:
            ui.show_message("Не удалось подключиться к базе данных")
    except Exception as error:
        ui.show_message(f'Произошла ошибка. {error}')
    finally:
        if db_conn:
            db_conn.close()
            ui.show_message("Соединение с базой данных закрыто")


if __name__ == '__main__':
    main()
