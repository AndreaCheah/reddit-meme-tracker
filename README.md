# Setup

1) Required environment variables:     
        `SUPABASE_URL`, 
        `SUPABASE_KEY`, 
        `CLIENT_ID`, 
        `CLIENT_SECRET`, 
        `USER_AGENT`, 
        `TELEGRAM_BOT_TOKEN`
1) `python -m venv venv`
2) `venv\Scripts\activate` (Windows)
3) `pip install requirements.txt`
4) `uvicorn api.main:app --reload`
5) Go to telegram, search for username @reddit_meme_tracker_bot and send any random message.
5) In another terminal, run `venv\Scripts\activate` and `python main.py`
