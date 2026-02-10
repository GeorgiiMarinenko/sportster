import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")  # URL, по которому будет открыт Mini App

if not BOT_TOKEN:
    raise RuntimeError("Не указан BOT_TOKEN в .env")
