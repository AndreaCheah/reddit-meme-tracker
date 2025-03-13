import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()

    required_env_vars = [
        "SUPABASE_URL", 
        "SUPABASE_KEY", 
        "CLIENT_ID", 
        "CLIENT_SECRET", 
        "USER_AGENT", 
        "TELEGRAM_BOT_TOKEN"
    ]

    for var in required_env_vars:
        if os.getenv(var) is None:
            print(f"Warning: {var} is not set in the environment.")
