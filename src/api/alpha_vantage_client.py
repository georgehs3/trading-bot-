import os
import requests
from dotenv import load_dotenv

load_dotenv()


class AlphaVantageClient:
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"

        if not self.api_key:
            raise ValueError("Missing ALPHA_VANTAGE_API_KEY in .env file!")

    def get_financial_news(self, tickers="AAPL,GOOGL,MSFT"):
        """Fetches financial news headlines for given stock tickers."""
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": tickers,
            "apikey": self.api_key,
        }

        response = requests.get(self.base_url, params=params)
        if response.status_code != 200:
            raise Exception(f"Alpha Vantage API Error: {response.text}")

        return response.json()

    def get_news_sentiment(self, stock_list):
        """Fetches news sentiment for multiple stock symbols from Alpha Vantage."""
        news_sentiment_data = {}

        for symbol in stock_list:
            params = {
                "function": "NEWS_SENTIMENT",
                "tickers": symbol,
                "apikey": self.api_key,
            }

            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                news_sentiment_data[symbol] = data.get("feed", [])
            else:
                news_sentiment_data[symbol] = []  # Handle API failures gracefully

        return news_sentiment_data


# Example usage
if __name__ == "__main__":
    av_client = AlphaVantageClient()
    news = av_client.get_financial_news()
    print(news)

    sentiment = av_client.get_news_sentiment(["AAPL", "TSLA"])
    print(sentiment)

