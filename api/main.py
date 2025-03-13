from fastapi import FastAPI
from services.meme_scraper import fetch_top_20_memes

app = FastAPI()

@app.get("/top-memes")
async def get_top_memes():
    return await fetch_top_20_memes()
