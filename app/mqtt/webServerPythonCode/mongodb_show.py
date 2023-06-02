from pymongo import MongoClient

# MongoDB client setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["mqtt_data"]
collection = db["device_data"]

def print_db_data(collection):
    for document in collection.find():
        print(document)

print_db_data(collection)
