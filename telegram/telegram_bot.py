import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def get_telegram_chat_id():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    
    try:
        data = response.json()
        return data["result"][0]["message"]["chat"]["id"] if data["result"] else None
    except Exception as error:
        print(f"Error fetching chat ID: {error}")
        return None

def send_report(telegram_chat_id, file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as file:
        requests.post(url, data={"chat_id": telegram_chat_id}, files={"document": file})

    print("PDF Report sent via Telegram!")
