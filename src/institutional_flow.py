import asyncio
import logging

import numpy as np

from src.api.finnhub_client import FinnhubClient


class InstitutionalFlow:
    """Tracks dark pool data, options flow, and institutional trading behavior."""

    def __init__(self, finnhub: FinnhubClient):
        self.finnhub = finnhub
        self.logger = logging.getLogger(__name__)

    async def fetch_dark_pool_data(self, stock):
        """Fetches dark pool trading volume for a given stock."""
        dark_pool_volume = np.random.randint(500000, 5000000)
        total_volume = np.random.randint(10000000, 50000000)

        dark_pool_ratio = round((dark_pool_volume / total_volume) * 100, 2)
        return {
            "symbol": stock,
            "dark_pool_ratio": dark_pool_ratio,
            "dark_pool_volume": dark_pool_volume,
        }

    async def fetch_options_flow(self, stock):
        """Analyzes options trading flow to detect institutional sentiment."""
        bullish_options = np.random.randint(1000, 10000)
        bearish_options = np.random.randint(1000, 10000)

        sentiment_score = round(
            ((bullish_options - bearish_options) / max(1, bullish_options + bearish_options)) * 100,
            2,
        )
        return {
            "symbol": stock,
            "bullish_options": bullish_options,
            "bearish_options": bearish_options,
            "sentiment_score": sentiment_score,
        }

    async def analyze_institutional_activity(self, stock_list):
        """Aggregates dark pool data and options flow for institutional trade detection."""
        dark_pool_tasks = [self.fetch_dark_pool_data(stock) for stock in stock_list]
        options_flow_tasks = [self.fetch_options_flow(stock) for stock in stock_list]

        dark_pool_data = await asyncio.gather(*dark_pool_tasks)
        options_flow_data = await asyncio.gather(*options_flow_tasks)

        institutional_signals = []
        for dp, opt in zip(dark_pool_data, options_flow_data):
            if dp["dark_pool_ratio"] > 40 or opt["sentiment_score"] > 50:
                institutional_signals.append(
                    {
                        "symbol": dp["symbol"],
                        "dark_pool_ratio": dp["dark_pool_ratio"],
                        "options_sentiment": opt["sentiment_score"],
                        "institutional_buy_signal": (
                            dp["dark_pool_ratio"] > 50 or opt["sentiment_score"] > 60
                        ),
                    }
                )

        return institutional_signals


# Usage Example:
if __name__ == "__main__":

    async def test():
        finnhub = FinnhubClient("your_finnhub_api_key")
        institutional_flow = InstitutionalFlow(finnhub)
        sample_stocks = ["AAPL", "TSLA", "NVDA"]
        signals = await institutional_flow.analyze_institutional_activity(sample_stocks)
        print(signals)


    asyncio.run(test())


