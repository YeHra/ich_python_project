import ui_gem as ui
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

        # Получаем подмножество данных для текущей страницы
        page_data = results[start_index:end_index]

        if not page_data:
            print("Все результаты показаны.")
            break

        print(f"\n--- Результаты ({start_index + 1}-{end_index} из {total_results}) ---")
        ui.print_table_data(headers, page_data)

        # Проверяем, есть ли еще данные для показа
        if end_index >= total_results:
            print("Все результаты показаны.")
            break

        # Спрашиваем пользователя, хочет ли он продолжить
        if not ui.ask_for_pagination():
            break

        current_page += 1
test_data = [(i,) for i in range(1, 25)]  # 24 элемента
test_headers = ["Number"]
#paginator(test_headers, test_data)
print(test_data)