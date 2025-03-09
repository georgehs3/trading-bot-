import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ✅ API Keys
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ✅ Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Ensure all required credentials exist
required_keys = {
    "FINNHUB_API_KEY": FINNHUB_API_KEY,
    "ALPHA_VANTAGE_API_KEY": ALPHA_VANTAGE_API_KEY,
    "DATABASE_URL": DATABASE_URL,
    "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
    "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
}

for key, value in required_keys.items():
    if not value:
        raise ValueError(f"Missing required environment variable: {key}")

# ✅ API Rate Limits
RATE_LIMITS = {
    "finnhub": 150,  # Requests per minute
    "alpha_vantage": 75,  # Requests per minute
}

# ✅ Trading Strategy Settings
TRADE_SETTINGS = {
    "SENTIMENT_THRESHOLD": 25,  # ✅ Sentiment score required for a trade signal (Lowered from 60)
    "PRICE_FLEXIBILITY": 0.95,  # ✅ Trade allowed if price is within 95% of high price
    "TIME_DECAY_FACTOR": 7,  # ✅ News older than 7 days loses influence
}

# ✅ Stock Selection Settings
STOCK_TRACKING = {
    "TOP_STOCKS": 50,  # ✅ Dynamically selects top 50 stocks
    "UPDATE_FREQUENCY": "weekly",  # ✅ Stocks refresh every week
    "SECTOR_FOCUS": ["Technology", "Energy", "Finance", "Healthcare"],  # ✅ Sector priority
}

# ✅ Logging Configuration
LOGGING = {
    "LEVEL": "INFO",  # Can be set to DEBUG for more details
    "FORMAT": "%(asctime)s - %(levelname)s - %(message)s",
}

# ✅ Market Tracking (Pre/Post Market)
MARKET_HOURS = {
    "PRE_MARKET": (4, 9, 30),  # 4:00 AM - 9:30 AM EST
    "REGULAR_MARKET": (9, 30, 16),  # 9:30 AM - 4:00 PM EST
    "POST_MARKET": (16, 20),  # 4:00 PM - 8:00 PM EST
}

# ✅ AI Learning Settings (Future Update)
AI_LEARNING = {
    "ENABLE_TRADE_LOGGING": True,  # ✅ Store trade history for improvement
    "MODEL_UPDATE_FREQUENCY": "daily",  # ✅ AI will adjust trading strategy daily
}

