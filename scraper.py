import praw
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()

reddit = praw.Reddit(
  client_id=os.getenv("CLIENT_ID"),
  client_secret=os.getenv("CLIENT_SECRET"),
  user_agent=os.getenv("USER_AGENT")
)

def get_top_20_memes():
  subreddit = reddit.subreddit("memes")
  crawled_time = datetime.now(timezone.utc)
  time_at_24h_ago = crawled_time - timedelta(hours=24)
  memes = []

  # get top posts ranked by Reddit, some may be older than 24 hours
  for post in subreddit.top(time_filter="day", limit=100):
    post_time = datetime.fromtimestamp(post.created_utc, tz=timezone.utc) # ensure utc

    if post_time >= time_at_24h_ago:
        memes.append({
          "id": post.id,
          "title": post.title,
          "score": post.score,
          "num_comments": post.num_comments,
          "url": f"https://www.reddit.com{post.permalink}",
          "image_url": post.url if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')) else None,  # TODO: double check
          "over_18": post.over_18,
          "upvote_ratio": post.upvote_ratio,
          "crawled_at": crawled_time.isoformat(),
          "created_at": post_time.isoformat(),
        })
    
    if len(memes) >= 20:
        break

  for rank, post in enumerate(memes, start=1):
    post["rank"] = rank

  return memes

# print(f"reddit.read_only: {reddit.read_only}")  # Should print: True
memes = get_top_20_memes()
print(memes[0]["created_at"])
# print(memes[0]["created_at"].isoformat())
# print(memes)
