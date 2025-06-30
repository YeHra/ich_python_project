import settings
import sys
sys.path.insert(0,"/home/user1/Документы/ICH/Python/myenv/lib/python3.12/site-packages")
from pymongo import MongoClient
client = MongoClient(settings.DATABASE_MONGO_W)

db_mongo = client[settings.DATABASE_MONGO_NAME]
search_info = db_mongo[settings.COLLECTION_MONGO_NAME]
client.admin.command("ping")
print("Connection successful!")
def five_latest_query():
    five_latest_search = []
    for doc in search_info.find().sort("timestamp", -1).limit(5):
        five_latest_search.append(doc)
    return five_latest_search
res = five_latest_query()


def five_popular_query():
    five_search = []
    five_popular_search = list(search_info.aggregate([{'$group':{'_id': "$params.category",'count_category': {'$sum': 1}}},{'$sort': {'count_category': -1}},{'$limit':5}]))
    for doc in five_popular_search:
        five_search.append(doc)
    return five_popular_search
res1 = five_popular_query()
