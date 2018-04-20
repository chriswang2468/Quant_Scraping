import pymongo
from pymongo import MongoClient
def localMongo():
	MONGO_DB = "Quant_database"
	client = MongoClient('localhost', 27017)
	db = client[MONGO_DB]
	return db