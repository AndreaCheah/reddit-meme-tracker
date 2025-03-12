import asyncio
from generate_report import fetch_memes_from_api, generate_report
from telegram_bot import get_telegram_chat_id, send_report_via_telegram

API_URL = "http://127.0.0.1:8000/top-memes"


async def generate_and_send_report():
    print("Fetching memes...")
    memes = fetch_memes_from_api(API_URL)

    if not memes:
        print("No memes available. Exiting.")
        return

    print("Generating report...")
    report_file = generate_report(memes)

    if not report_file:
        print("Failed to generate report. Exiting.")
        return

    print("Fetching Telegram Chat ID...")
    telegram_chat_id = get_telegram_chat_id()

    if not telegram_chat_id:
        print("Cannot send report. No chat ID found.")
        return

    print("Sending report via Telegram...")
    await send_report_via_telegram(telegram_chat_id, report_file)


if __name__ == "__main__":
    asyncio.run(generate_and_send_report())
