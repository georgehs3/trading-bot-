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
