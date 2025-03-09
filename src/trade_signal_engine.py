import asyncio
import datetime
import logging
import numpy as np
from transformers import pipeline  # Hugging Face BERT for sentiment analysis
from src.api.alpha_vantage_client import AlphaVantageClient
from src.api.finnhub_client import FinnhubClient


class TradeSignalEngine:
    """Processes stock data, news sentiment, and AI analysis to generate high-confidence trade signals."""

    def __init__(self, finnhub: FinnhubClient, alpha_vantage: AlphaVantageClient):
        self.finnhub = finnhub
        self.alpha_vantage = alpha_vantage
        self.logger = logging.getLogger(__name__)
        self.sentiment_analyzer = pipeline("sentiment-analysis")  # Using BERT NLP model

    async def fetch_market_data(self, stock_list):
        """Fetch real-time stock data in batches to avoid rate limits."""
        batch_size = 10
        market_data = []

        for i in range(0, len(stock_list), batch_size):
            batch = stock_list[i : i + batch_size]
            self.logger.info(f"Fetching market data for batch {i // batch_size + 1} of {len(stock_list) // batch_size + 1}...")

            tasks = [self.finnhub.get_stock_price(stock) for stock in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for stock, result in zip(batch, results):
                if isinstance(result, Exception):
                    self.logger.warning(f"Error fetching data for {stock}: {result}")
                else:
                    market_data.append(result)

        self.logger.info(f"Fetched market data for {len(market_data)} stocks.")
        return market_data

    async def fetch_news_sentiment(self, stock_list):
        """Fetch sentiment analysis for news related to the given stock list."""
        self.logger.info(f"Fetching news sentiment for {len(stock_list)} stocks...")
        news_sentiment = self.alpha_vantage.get_news_sentiment(stock_list)

        if not news_sentiment:
            self.logger.warning("No news sentiment data returned.")

        self.logger.info(f"Fetched sentiment for {len(news_sentiment)} stocks.")
        return news_sentiment

    def calculate_trade_influence_score(self, news_data):
        """Assigns a 0-100% Trade Influence Score based on sentiment, credibility, recency, and historical impact."""
        score = 0
        if not news_data:
            return score  # No impact if no news is available

        sentiment_scores = []
        for news in news_data:
            headline = news.get("headline") or news.get("title")  # ✅ Use "title" if "headline" is missing
            if not headline:
                self.logger.warning(f"Skipping news entry without headline/title: {news}")
                continue

            sentiment = self.sentiment_analyzer(headline)[0]
            sentiment_strength = sentiment["score"]
            recency_weight = max(
                0,
                1 - ((datetime.datetime.utcnow() - news.get("date", datetime.datetime.utcnow())).days / 7),
            )  # Decay over a week
            credibility_weight = (
                1.0 if news.get("source", "") in ["Reuters", "Bloomberg", "CNBC"] else 0.5
            )
            historical_impact = (
                0.8 if "earnings" in headline.lower() else 0.5
            )  # Higher impact for earnings

            trade_score = (
                sentiment_strength
                * recency_weight
                * credibility_weight
                * historical_impact
                * 100
            )
            sentiment_scores.append(trade_score)

        return round(np.mean(sentiment_scores), 2) if sentiment_scores else 0

    def generate_trade_signals(self, market_data, news_sentiment):
        """Generates trade signals based on price trends, sentiment, and AI-based pattern detection."""
        trade_signals = []

        for stock in market_data:
            if not stock:
                continue  # Skip invalid data

            sentiment_score = self.calculate_trade_influence_score(
                news_sentiment.get(stock["symbol"], [])
            )

            # ✅ Log stock prices and sentiment for debugging
            self.logger.info(
                f"Stock: {stock['symbol']}, Price: {stock['current_price']}, High: {stock['high_price']}, Sentiment: {sentiment_score}"
            )

            # ✅ Applied both improvements:
            # - Lowered Sentiment Threshold to 25 (was 60)
            # - Increased Market Price Flexibility to 95% of high price (was 98%)
            if (
                stock["current_price"] > stock["high_price"] * 0.95
                and sentiment_score > 25
            ):
                trade_signals.append(
                    {
                        "symbol": stock["symbol"],
                        "action": "BUY",
                        "entry_range": (
                            stock["current_price"],
                            stock["high_price"] * 1.02,
                        ),
                        "stop_loss": stock["low_price"] * 0.98,
                        "take_profit": stock["current_price"] * 1.03,
                        "confidence": sentiment_score,
                    }
                )

        self.logger.info(f"Generated {len(trade_signals)} trade signals.")
        return trade_signals

    async def run(self, stock_list):
        """Runs the TradeSignalEngine to fetch data, analyze sentiment, and generate trade signals."""
        self.logger.info(f"Fetching market data for {len(stock_list)} stocks...")
        market_data = await self.fetch_market_data(stock_list)

        self.logger.info(f"Fetching news sentiment for {len(stock_list)} stocks...")
        news_sentiment = await self.fetch_news_sentiment(stock_list)

        self.logger.info(f"Fetched {len(market_data)} market data entries.")
        self.logger.info(f"Fetched sentiment for {len(news_sentiment)} stocks.")

        self.logger.info("Generating trade signals...")
        trade_signals = self.generate_trade_signals(market_data, news_sentiment)

        self.logger.info(f"Generated {len(trade_signals)} trade signals.")
        return trade_signals

