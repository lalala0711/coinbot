import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import requests
import os
import json

client = MongoClient("mongodb+srv://hwko0023:MikaelLevi0095@coingecko.fdzor.mongodb.net/")
db = client['coingecko']
collection = db['coins']

df = pd.json_normalize(list(collection.find()), sep="_")
dfsliced = df[['dateInserted', 'last_updated', 'id', 'symbol', 'name', 'market_data_current_price_php']]
dfsliced['last_updated'] = pd.to_datetime(dfsliced['last_updated']) 
dfsliced['dateInserted'] = pd.to_datetime(dfsliced['dateInserted']).dt.tz_localize('UTC', ambiguous='NaT', nonexistent='NaT')
dfsliced['realDate'] = np.where(
    dfsliced['last_updated'].isna(), 
    dfsliced['dateInserted'], 
    dfsliced['last_updated'])
# dfsliced['realDate'] = dfsliced['realDate'].dt.date

doge = dfsliced[dfsliced['symbol'] == 'doge']
doge = doge.sort_values(by='realDate')

plt.figure(figsize=(12, 6))
plt.plot(doge['realDate'], doge['market_data_current_price_php'], label='Dogecoin Price in PHP', color='blue')

plt.title('Dogecoin Price Over Time (PHP)')
plt.xlabel('Date')
plt.ylabel('Price (PHP)')
plt.legend()
plt.grid(True)
for i, row in doge.iterrows():
    plt.annotate(
        f"{row['market_data_current_price_php']:.2f}",
        (row['realDate'], row['market_data_current_price_php']),
        textcoords="offset points",
        xytext=(0,5),
        ha='center',
        fontsize=8,
        color='black'
    )

plt.show()