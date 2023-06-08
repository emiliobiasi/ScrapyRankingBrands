import json
from pymongo import MongoClient


with open('marcas.json', 'r') as file:
    data = json.load(file)


client = MongoClient('mongodb+srv://giandutra:giandutra@cluster0.xdo5ska.mongodb.net/?retryWrites=true&w=majority')
database = client['brands']  
collection = database['marcas']  


collection.insert_many(data)


client.close()
