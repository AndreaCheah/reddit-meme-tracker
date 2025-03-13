from datetime import datetime, timezone

def generate_meme_report(memes, visualization_path):
    if not memes:
        print("No memes available to generate a report.")
        return None

    report_filename = f"top_memes_report_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    with open(report_filename, "w", encoding="utf-8") as file:
        file.write("Top 20 Trending Memes Report (Past 24 Hours)\n")
        file.write("=" * 50 + "\n\n")
        
        for meme in memes:
            file.write(f"Rank: {meme['rank']}\n")
            file.write(f"Title: {meme['title']}\n")
            file.write(f"Score: {meme['score']}\n")
            file.write(f"Comments: {meme['num_comments']}\n")
            file.write(f"Upvote Ratio: {meme['upvote_ratio']}\n")
            file.write(f"URL: {meme['url']}\n")
            file.write(f"Created At: {meme['created_at']}\n")
            file.write("-" * 50 + "\n")

    print(f"Report generated: {report_filename}")
    return report_filename, visualization_path
