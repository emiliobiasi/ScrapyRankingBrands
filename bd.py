import json
from pymongo import MongoClient


def bd():
    with open('marcas.json', 'r') as file:
        data = json.load(file)

    client = MongoClient(
        'mongodb+srv://<user>:<password>@cluster0.aharvcg.mongodb.net/?retryWrites=true&w=majority')
    database = client['brands']
    collection = database['marcas']

    collection.insert_many(data)

    client.close()
