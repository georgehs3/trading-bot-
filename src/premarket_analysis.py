import logging
import asyncio
import numpy as np
from src.api.finnhub_client import FinnhubClient

class PreMarketAnalysis:
    """Monitors early trends in pre-market trading to detect momentum shifts before market open."""

    def __init__(self, finnhub: FinnhubClient):
        self.finnhub = finnhub
        self.logger = logging.getLogger(__name__)

    async def fetch_premarket_data(self, stock_list):
        """Fetches pre-market trading data for given stocks."""
        tasks = [self.finnhub.get_stock_price(stock) for stock in stock_list]
        return await asyncio.gather(*tasks)

    def detect_gaps(self, current_price, prev_close):
        """Detects pre-market price gaps."""
        if not prev_close:
            return None

        gap_percent = ((current_price - prev_close) / prev_close) * 100
        return round(gap_percent, 2)

    def detect_unusual_premarket_activity(self, premarket_volume, avg_volume):
        """Identifies stocks with unusually high pre-market trading activity."""
        if avg_volume == 0:
            return False

        volume_ratio = premarket_volume / avg_volume
        return volume_ratio > 2.5  # Example threshold

    async def analyze_premarket_trends(self, stock_list):
        """Analyzes pre-market gaps and momentum shifts for trade setups."""
        premarket_data = await self.fetch_premarket_data(stock_list)
        trade_opportunities = []

        for stock in premarket_data:
            if not stock:
                continue

            price_gap = self.detect_gaps(stock["current_price"], stock["previous_close"])
            unusual_activity = self.detect_unusual_premarket_activity(stock["current_price"], stock["previous_close"])

            if price_gap and abs(price_gap) > 2.0 and unusual_activity:
                trade_opportunities.append({
                    "symbol": stock["symbol"],
                    "gap_percent": price_gap,
                    "pre_market_momentum": "Bullish" if price_gap > 0 else "Bearish"
                })

        return trade_opportunities

# Usage Example:
if __name__ == "__main__":
    async def test():
        finnhub = FinnhubClient("your_finnhub_api_key")
        premarket = PreMarketAnalysis(finnhub)
        sample_stocks = ["AAPL", "TSLA", "NVDA"]
        premarket_signals = await premarket.analyze_premarket_trends(sample_stocks)
        print(premarket_signals)

    asyncio.run(test())

