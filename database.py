from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import asyncio
from scraper import get_top_20_memes # TODO: remove later

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def store_memes_in_db(memes_list):
    if not memes_list:
        print("No memes to store in database.")
        return
    
    try:
        for meme in memes_list:
            response = supabase.table("memes").upsert(meme).execute()
            if "error" in response and response["error"]:
                print(f"Database Error: {response['error']}")
        
        print("Successfully stored memes in the database.")
    
    except Exception as e:
        print(f"Error storing memes in database: {e}")

if __name__ == "__main__":
    memes = asyncio.run(get_top_20_memes())
    data = asyncio.run(store_memes_in_db(memes))
