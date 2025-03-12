from fastapi import FastAPI
from scraper import get_top_20_memes
from database import store_memes_in_db

app = FastAPI()

@app.get("/top-memes")
def get_top_memes():
  top_memes = get_top_20_memes()
  store_memes_in_db(top_memes)
  return top_memes