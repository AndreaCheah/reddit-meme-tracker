import asyncpraw
import os
from datetime import datetime, timedelta, timezone
from utils.env_loader import load_environment

load_environment()

async def fetch_top_20_memes():
    try:
        async with asyncpraw.Reddit(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            user_agent=os.getenv("USER_AGENT")
        ) as reddit:

            subreddit = await reddit.subreddit("memes")
            collected_memes = []
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
            rank = 1

            async for post in subreddit.top(time_filter="day", limit=100):
                post_creation_time = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)

                if post_creation_time >= cutoff_time:
                    collected_memes.append({
                        "id": post.id,
                        "rank": rank,
                        "title": post.title,
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "url": f"https://www.reddit.com{post.permalink}",
                        "image_url": post.url if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')) else None,
                        "over_18": post.over_18,
                        "upvote_ratio": post.upvote_ratio,
                        "created_at": post_creation_time.isoformat(),
                        "crawled_at": datetime.now(timezone.utc).isoformat(),
                    })
                    rank += 1

                if len(collected_memes) >= 20:
                    break

            return collected_memes

    except Exception as e:
        print(f"Error fetching memes from Reddit: {e}")
        return []
