import asyncpraw
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
import asyncio

load_dotenv()

async def get_top_20_memes():
    try:
        async with asyncpraw.Reddit(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            user_agent=os.getenv("USER_AGENT")
        ) as reddit:

            subreddit = await reddit.subreddit("memes")
            
            crawled_time = datetime.now(timezone.utc)
            time_at_24h_ago = crawled_time - timedelta(hours=24)
            memes = []

            rank = 1
            async for post in subreddit.top(time_filter="day", limit=100):
                post_time = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)

                if post_time >= time_at_24h_ago:
                    memes.append({
                        "id": post.id,
                        "title": post.title,
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "url": f"https://www.reddit.com{post.permalink}",
                        "image_url": post.url if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')) else None,
                        "over_18": post.over_18,
                        "upvote_ratio": post.upvote_ratio,
                        "crawled_at": crawled_time.isoformat(),
                        "created_at": post_time.isoformat(),
                        "rank": rank
                    })
                    rank += 1

                if len(memes) >= 20:
                    break

            return memes

    except Exception as e:
        print(f"Error while fetching memes from Reddit: {e}")
        return []

if __name__ == "__main__":
    memes = asyncio.run(get_top_20_memes())
    print(memes)
