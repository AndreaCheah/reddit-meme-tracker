import requests
from datetime import datetime, timezone

TOP_MEMES_API_URL = "http://127.0.0.1:8000/top-memes"

def fetch_memes_from_api():
    try:
        response = requests.get(TOP_MEMES_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching memes from API: {response.status_code}")
            return []
    except Exception as e:
        print(f"Exception occurred while fetching memes: {e}")
        return []


def generate_report():
    memes = fetch_memes_from_api()

    if not memes:
        print("No memes available to generate report.")
        return None
    
    report_filename = f"top_memes_report_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    with open(report_filename, "w", encoding="utf-8") as file:
        file.write("Top 20 Trending Memes Report\n")
        file.write("=" * 40 + "\n\n")

        for meme in memes:
            file.write(f"Rank: {meme['rank']}\n")
            file.write(f"Title: {meme['title']}\n")
            file.write(f"Score: {meme['score']}\n")
            file.write(f"Comments: {meme['num_comments']}\n")
            file.write(f"Upvote Ratio: {meme['upvote_ratio']}\n")
            file.write(f"URL: {meme['url']}\n")
            file.write(f"Created At: {meme['created_at']}\n")
            file.write("-" * 40 + "\n")

    print(f"Report generated: {report_filename}")
    return report_filename


if __name__ == "__main__":
    report_file = generate_report()
