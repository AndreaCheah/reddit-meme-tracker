# Setup

1) Required environment variables:     
    - `SUPABASE_URL`  
    - `SUPABASE_KEY`  
    - `CLIENT_ID`  
    - `CLIENT_SECRET`  
    - `USER_AGENT`  
    - `TELEGRAM_BOT_TOKEN`  

2) Create a virtual environment:  
    ```sh
    python -m venv venv
    ```

3) Activate the virtual environment:  
    - Windows:  
      ```sh
      venv\Scripts\activate
      ```
    - macOS/Linux:  
      ```sh
      source venv/bin/activate
      ```

4) Install dependencies:  
    ```sh
    pip install -r requirements.txt
    ```

5) Start the API server:  
    ```sh
    uvicorn api.main:app --reload
    ```

6) Go to Telegram, search for username `@reddit_meme_tracker_bot`, and send any random message.

7) In another terminal, activate the virtual environment and run the script:  
    ```sh
    venv\Scripts\activate  # Windows
    source venv/bin/activate  # macOS/Linux
    python main.py
    ```
    This will:  
    - Scrape the top 20 memes in the past 24 hours.  
    - Save the memes into the Supabase database.  
    - Generate a report containing the top 20 memes and data visualization graphs.  
