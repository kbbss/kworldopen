from pymongo import MongoClient


client = MongoClient('mongodb://kbs:kebi2077@210.114.1.177:27017')

db = client["kls"]