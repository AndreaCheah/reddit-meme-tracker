# Setup

1) Required environment variables:     
        `SUPABASE_URL`, 
        `SUPABASE_KEY`, 
        `CLIENT_ID`, 
        `CLIENT_SECRET`, 
        `USER_AGENT`, 
        `TELEGRAM_BOT_TOKEN`
2) `python -m venv venv`
3) `venv\Scripts\activate` (Windows)
4) `pip install requirements.txt`
5) `uvicorn api.main:app --reload`
6) Go to telegram, search for username @reddit_meme_tracker_bot and send any random message.
7) In another terminal, run `venv\Scripts\activate` and `python main.py`
