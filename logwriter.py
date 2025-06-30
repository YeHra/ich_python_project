from datetime import datetime
import settings
import sys
sys.path.insert(0,"/home/user1/Документы/ICH/Python/project/lib/python3.12/site-packages")
from pymongo import MongoClient

client = MongoClient(settings.DATABASE_MONGO_W)

db_mongo = client[settings.DATABASE_MONGO_NAME]
search_info = db_mongo[settings.COLLECTION_MONGO_NAME]


def search_log(search_type: str, params: dict, results_count: int):
    '''
    Функция записывает в коллекцию MongoDB словарь с данными пользовательского запроса
    :param search_type: Тип поиска (e.g., "keyword", "category_year", "category_range_year")
    :param params: Словарь с параметрами поиска (e.g., {"keyword": "test"}, {"category": "Action", "release_year": 2020})
    :param results_count: Количество найденных результатов
    '''
    search_object = {
        "timestamp": datetime.now(),
        "search_type": search_type,
        "params": params,
        "results_count": results_count
    }
    try:
        search_info.insert_one(search_object)
    except Exception as e:
        print(f"Error writing search log to MongoDB: {e}")


def five_last_query():
    """
    Возвращает список из пяти последних запросов из MongoDB, готовый для PrettyTable.
    """
    results = []
    try:
        for doc in search_info.find().sort("timestamp", -1).limit(5):
            doc['_id'] = str(doc['_id'])
            doc['timestamp'] = doc['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            results.append(doc)
    except Exception as e:
        print(f"Error retrieving five last queries from MongoDB: {e}")
    return results


def five_popular_query():
    """
    Возвращает список из пяти самых популярных запросов (по категории) из MongoDB, готовый для PrettyTable.
    """
    popular_searches = []
    try:
        popular_searches = list(search_info.aggregate([
            {'$match': {'search_type': {'$in': ['category_year', 'category_range_year']}}},
            {'$group': {'_id': "$params.category", 'count_category': {'$sum': 1}}},
            {'$sort': {'count_category': -1}},
            {'$limit': 5}
        ]))
    except Exception as e:
        print(f"Error retrieving five popular queries from MongoDB: {e}")

    formatted_results = [(doc['_id'], doc['count_category']) for doc in popular_searches]
    return formatted_results