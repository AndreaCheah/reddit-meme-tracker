from supabase import create_client
import os
from dotenv import load_dotenv
import asyncio
# from meme_scraper import scrape_top_20_memes

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def save_memes_to_db(memes_list):
    if not memes_list:
        print("No memes to store in the database.")
        return
    
    try:
        for meme in memes_list:
            response = supabase.table("memes").upsert(meme).execute()
            if "error" in response and response["error"]:
                print(f"Database Error: {response['error']}")
        
        print("Successfully stored memes in the database.")
    
    except Exception as error:
        print(f"Error storing memes in database: {error}")

# if __name__ == "__main__":
#   memes = asyncio.run(scrape_top_20_memes())
#   asyncio.run(save_memes_to_db(memes))