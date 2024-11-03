from pymongo import MongoClient
import pandas as pd
import os
import json
import smtplib
from email.mime.text import MIMEText
from config import load_environment_variables
import numpy as np

cfg = load_environment_variables()
mongodbpass = cfg['MONGODB_PASSWORD']
apppass = cfg['APP_PASSWORD']
apikey = os.environ.get('COINGECKO_API_KEY')

client = MongoClient(f"mongodb+srv://hwko0023:{mongodbpass}@coingecko.fdzor.mongodb.net/")
db = client['coingecko']
collection = db['coins']

workDir = os.getcwd()
# with open(os.path.join(workDir, "creds.json"), 'r') as file:
#     jsonCreds = json.load(file)

# Fetch all coins
df = pd.json_normalize(list(collection.find()), sep="_")
df = pd.json_normalize(list(collection.find()), sep="_")
df = df[['dateInserted', 'last_updated', 'id', 'symbol', 'name', 'market_data_current_price_php']]
df['last_updated'] = pd.to_datetime(df['last_updated']) 
df['dateInserted'] = pd.to_datetime(df['dateInserted']).dt.tz_localize('UTC', ambiguous='NaT', nonexistent='NaT')
df['realDate'] = np.where(
    df['last_updated'].isna(), 
    df['dateInserted'], 
    df['last_updated'])
# df['realDate'] = df['realDate'].dt.date
df.sort_values('realDate', ascending=False, inplace=True)
df = df[~df['id'].isna()]
df = df.drop_duplicates(subset=['id'])

# Load target prices from CSV
dfgoals = pd.read_csv('coinLimits.csv')

def send_email(subject, message_text, recipient_email):
    email_user = 'hwko0023@gmail.com'
    email_password = apppass
    email_to = recipient_email

    # Create the email message
    msg = MIMEText(message_text, "html")  # Use HTML for better formatting
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = email_to

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade to a secure connection
            server.login(email_user, email_password)
            server.sendmail(email_user, email_to, msg.as_string())
            print("Email sent!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Build the message body
message_body = "<h1>Coin Price Alerts</h1>"
message_body += "<table border='1'><tr><th>Coin</th><th>Target Price</th><th>Current Price</th></tr>"

for index, row in df.iterrows():
    coin_id = row['id']
    current_price = row['market_data_current_price_php']
    
    # Get the target price from dfgoals
    target_price_row = dfgoals[dfgoals['Coins ID'] == coin_id]
    
    if not target_price_row.empty:
        target_price = target_price_row['My Target Price'].values[0]

        # Check if the current price meets or exceeds the target price
        # if current_price >= target_price:
        message_body += f"<tr><td>{coin_id}</td><td>{target_price}</td><td>{current_price}</td></tr>"

message_body += "</table>"

# Send email with all coin information
send_email("Coin Price Alert", message_body, "hwko0023@gmail.com")
