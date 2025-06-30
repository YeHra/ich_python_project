from datetime import datetime
import settings
import sys


sys.path.insert(0,"/home/user1/Документы/ICH/Python/myenv/lib/python3.12/site-packages")
from pymongo import MongoClient
client = MongoClient(settings.DATABASE_MONGO_W)

db_mongo = client[settings.DATABASE_MONGO_NAME]
search_info = db_mongo[settings.COLLECTION_MONGO_NAME]
client.admin.command("ping")

def five_last_query():
    five_last_search = []
    for doc in search_info.find().sort("timestamp", -1).limit(5):
        five_last_search.append(doc)
    return five_last_search
five_last_query_res = five_last_query()