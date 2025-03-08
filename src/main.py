import sys
import os
import yaml
import logging
import asyncio
from dotenv import load_dotenv
from src.api.finnhub_client import FinnhubClient
from src.api.alpha_vantage_client import AlphaVantageClient
from src.trade_signal_engine import TradeSignalEngine
from src.utils.async_requests import RequestScheduler
from src.alerts.alert_manager import AlertManager
from src.database.db_connector import DatabaseConnector

# Ensure the script can find the `src/` package
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# Load environment variables
load_dotenv()

# Retrieve API keys
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Validate API keys exist
if not FINNHUB_API_KEY or not ALPHA_VANTAGE_API_KEY:
    raise ValueError("Missing API keys! Check your .env file.")

# Initialize API Clients
finnhub_client = FinnhubClient()
alpha_vantage_client = AlphaVantageClient()

# Define API rate limits
rate_limits = {
    "finnhub": 150,  # Finnhub rate limit per minute
    "alpha_vantage": 75  # Alpha Vantage rate limit per minute
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

