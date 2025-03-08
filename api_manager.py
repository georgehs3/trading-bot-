# File: api_manager.py
# Purpose: Handles real-time stock & news data requests asynchronously

import aiohttp
import asyncio
import time

# Finnhub & Alpha Vantage API Keys (Replace with your actual API keys)
FINNHUB_API_KEY = "your_finnhub_api_key"
ALPHA_VANTAGE_API_KEY = "your_alpha_vantage_api_key"

# API Rate Limits
FINNHUB_RATE_LIMIT = 150  # 150 requests per minute
ALPHA_VANTAGE_RATE_LIMIT = 75  # 75 requests per minute

class APIManager:
    def __init__(self):
        self.finnhub_semaphore = asyncio.Semaphore(FINNHUB_RATE_LIMIT)
        self.alpha_vantage_semaphore = asyncio.Semaphore(ALPHA_VANTAGE_RATE_LIMIT)

    async def fetch(self, session, url, headers=None):
        """Handles API requests with rate limiting"""
        async with session.get(url, headers=headers) as response:
            return await response.json()

    async def get_stock_data(self, symbol):
        """Fetches stock price data from Finnhub"""
        async with self.finnhub_semaphore:
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
            async with aiohttp.ClientSession() as session:
                return await self.fetch(session, url)

    async def get_news_sentiment(self, symbol):
        """Fetches stock-related news sentiment from Alpha Vantage"""
        async with self.alpha_vantage_semaphore:
            url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
            async with aiohttp.ClientSession() as session:
                return await self.fetch(session, url)

async def main():
    """Example usage of APIManager"""
    api_manager = APIManager()
    stock_data = await api_manager.get_stock_data("AAPL")
    news_sentiment = await api_manager.get_news_sentiment("AAPL")

    print("Stock Data:", stock_data)
    print("News Sentiment:", news_sentiment)

# Run the script asynchronously
if __name__ == "__main__":
    asyncio.run(main())

