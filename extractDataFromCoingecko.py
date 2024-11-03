from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import requests
import os
import json

client = MongoClient("mongodb+srv://hwko0023:MikaelLevi0095@coingecko.fdzor.mongodb.net/")
db = client['coingecko']
collection = db['coins']

workDir = os.getcwd()
with open(os.path.join(workDir, "creds.json"), 'r') as file:
    jsonCreds = json.load(file)

df = pd.read_csv("coinLimits.csv")

def insertCoinToMongo(coinid):
    url = f'https://api.coingecko.com/api/v3/coins/{coinid}'
    r = requests.get(
        url,
        headers={
            "accept": "application/json",
            "x-cg-demo-api-key": jsonCreds['API Key']
        }
    )
    data = r.json()
    dateInserted = {
        "dateInserted": datetime.now(),
        "mySearch": coinid
    }
    dateInserted.update(data)
    collection.insert_one(dateInserted)
    print(f"{coinid} done")

for i, x in df.iterrows():
    insertCoinToMongo(x['Coins ID'])