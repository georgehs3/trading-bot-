import aiohttp
import os
import finnhub
from dotenv import load_dotenv

load_dotenv()


class FinnhubClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY")
        if not self.api_key:
            raise ValueError("Missing Finnhub API key! Add it to .env")

        self.client = finnhub.Client(api_key=self.api_key)

    def get_stock_quote(self, symbol):
        """Fetch latest stock quote"""
        return self.client.quote(symbol)

    def get_news_sentiment(self, symbol):
        """Fetch relevant news for sentiment analysis"""
        return self.client.company_news(symbol, _from="2024-01-01", to="2024-12-31")

    async def get_stock_price(self, symbol):
        """Fetches stock price asynchronously using Finnhub API."""
        async with aiohttp.ClientSession() as session:
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={self.api_key}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "symbol": symbol,
                        "current_price": data.get("c"),
                        "high_price": data.get("h"),
                        "low_price": data.get("l"),
                    }
                return None  # Handle API failures gracefully

