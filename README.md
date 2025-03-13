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
5) In another terminal, run `python main.py`
