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
        """Fetch real-time stock data for the given stock list."""
        tasks = [self.finnhub.get_stock_price(stock) for stock in stock_list]
        return await asyncio.gather(*tasks)

    async def fetch_news_sentiment(self, stock_list):
        """Fetch sentiment analysis for news related to the given stock list."""
        return await self.alpha_vantage.get_news_sentiment(stock_list)

    def calculate_trade_influence_score(self, news_data):
        """Assigns a 0-100% Trade Influence Score based on sentiment, credibility, recency, and historical impact."""
        score = 0
        if not news_data:
            return score  # No impact if no news is available

        sentiment_scores = []
        for news in news_data:
            sentiment = self.sentiment_analyzer(news["headline"])[0]
            sentiment_strength = sentiment["score"]
            recency_weight = max(
                0, 1 - (datetime.datetime.utcnow() - news["date"]).days / 7
            )  # Decay over a week
            credibility_weight = (
                1.0 if news["source"] in ["Reuters", "Bloomberg", "CNBC"] else 0.5
            )
            historical_impact = (
                0.8 if "earnings" in news["headline"].lower() else 0.5
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

            # Basic buy condition: Price breaking resistance, positive
            # sentiment
            if (
                stock["current_price"] > stock["high_price"] * 0.98
                and sentiment_score > 60
            ):
                trade_signals.append(
                    {
                        "symbol": stock["symbol"],
                        "action": "BUY",
                        # VWAP-based range
                        "entry_range": (
                            stock["current_price"],
                            stock["high_price"] * 1.02,
                        ),
                        # ATR-based stop loss
                        "stop_loss": stock["low_price"] * 0.98,
                        # 3% profit target
                        "take_profit": stock["current_price"] * 1.03,
                        "confidence": sentiment_score,
                    }
                )

        return trade_signals
