import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GET_UPDATES_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"


def get_telegram_chat_id() -> int:
    response = requests.get(TELEGRAM_GET_UPDATES_URL)

    try:
        data = response.json()
        if "result" in data and len(data["result"]) > 0:
            chat_id = data["result"][0]["message"]["chat"]["id"]  # retrieve chat id from nested JSON data
            return chat_id

        else:
            print("No chat ID found. Send a message to @reddit_meme_tracker_bot first!")
            return None
    
    except Exception as e:
        print(f"Error fetching chat ID: {e}")
        return None
    

async def send_report_via_telegram(telegram_chat_id: int, filepath: str) -> None:
    if not telegram_chat_id:
        print("Failed to retrieve Telegram chat ID. Exiting.")
        return None
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"

    with open(filepath, "rb") as file:
        response = requests.post(url, data={"chat_id": telegram_chat_id}, files={"document": file})

    if response.status_code == 200:
        print("Report sent successfully via Telegram!")
    else:
        print(f"Error sending report: {response.json()}")
