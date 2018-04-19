from sshtunnel import SSHTunnelForwarder
import pymongo

def mongoConnection(server):
	MONGO_DB = "Quant_database"
	client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
	db = client[MONGO_DB]
	return db
	# pprint.pprint(db.collection_names())

	# server.stop()

def setServer():
	MONGO_HOST = "13.58.236.43"
	MONGO_DB = "Quant_database"
	MONGO_USER = "admin"
	MONGO_PASS = "admin"
	server = SSHTunnelForwarder(
	    MONGO_HOST,
	    ssh_username='chris',
	    ssh_password='wang0408',
	    remote_bind_address=('127.0.0.1', 27017)
	)
	return server