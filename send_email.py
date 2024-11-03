import smtplib
from email.mime.text import MIMEText
import pandas as pd
import requests
import json
import os

workDir = os.getcwd()
with open(os.path.join(workDir, "creds.json"), 'r') as file:
    jsonCreds = json.load(file)

def send_email(subject, message_text, recipient_email):
    email_user = 'hwko0023@gmail.com'
    email_password = jsonCreds['App Password']
    email_to = recipient_email

    # Create the email message
    msg = MIMEText(message_text)
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

# Example usage
send_email("Crypto Price Alert", "Your target price has been reached!", "hwko0023@gmail.com")
