import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Bot configuration
BOT_NAME = "BypasnksBOT"
BOT_VERSION = "1.0"

# Timeout settings
REQUEST_TIMEOUT = 30
BROWSER_TIMEOUT = 60
