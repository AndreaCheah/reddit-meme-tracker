from fastapi import FastAPI
from scraper import get_top_20_memes

app = FastAPI()

@app.get("/top-memes")
async def get_top_memes():
    top_memes = await get_top_20_memes()
    return top_memes