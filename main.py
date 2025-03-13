import asyncio
from fetcher.fetch_memes import fetch_memes
from services.meme_visualisation import gen_upvotes_vs_comments_graph, gen_fastest_rising_memes_graph
from services.meme_report import generate_meme_report
from telegram.telegram_bot import get_telegram_chat_id, send_report

async def main():
    print("Fetching memes...")
    memes = fetch_memes()
    if not memes:
        print("No memes available. Exiting.")
        return

    print("Generating visualization...")
    visualization_path = gen_upvotes_vs_comments_graph(memes)
    rising_meme_path = gen_fastest_rising_memes_graph(memes)

    print("Generating report...")
    report_path = generate_meme_report(memes, visualization_path, rising_meme_path)

    print("Fetching Telegram Chat ID...")
    chat_id = get_telegram_chat_id()
    if not chat_id:
        print("Cannot send report. No chat ID found.")
        return

    print("Sending report via Telegram...")
    send_report(chat_id, report_path)

if __name__ == "__main__":
    asyncio.run(main())
