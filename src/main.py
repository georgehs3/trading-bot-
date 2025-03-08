import asyncio
import logging
import os

from dotenv import load_dotenv

from src.alerts.alert_manager import AlertManager
from src.api.alpha_vantage_client import AlphaVantageClient
from src.api.finnhub_client import FinnhubClient
from src.database.db_connector import DatabaseConnector
from src.trade_signal_engine import TradeSignalEngine
from src.utils.async_requests import RequestScheduler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Retrieve API keys
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Validate API keys exist
if not FINNHUB_API_KEY or not ALPHA_VANTAGE_API_KEY:
    raise ValueError("Missing API keys! Check your .env file.")

# Initialize API Clients with the correct API keys
finnhub_client = FinnhubClient(api_key=FINNHUB_API_KEY)
alpha_vantage_client = AlphaVantageClient()

# Define API rate limits
rate_limits = {
    "finnhub": 150,  # Finnhub rate limit per minute
    "alpha_vantage": 75,  # Alpha Vantage rate limit per minute
}

# Initialize components
request_scheduler = RequestScheduler(rate_limits)
trade_signal_engine = TradeSignalEngine(finnhub_client, alpha_vantage_client, request_scheduler)
alert_manager = AlertManager()
db_connector = DatabaseConnector()


async def main():
    logging.info("Starting trading bot...")

    # Fetch market data & analyze trades
    await trade_signal_engine.run()

    # Monitor alerts
    await alert_manager.monitor_alerts()


if __name__ == "__main__":
    asyncio.run(main())

