import logging
import asyncio
import numpy as np
from src.api.finnhub_client import FinnhubClient

class MarketBreadth:
    """Analyzes market-wide sentiment, sector strength, and risk conditions."""

    def __init__(self, finnhub: FinnhubClient):
        self.finnhub = finnhub
        self.logger = logging.getLogger(__name__)

    async def fetch_advance_decline_data(self):
        """Fetches the advance/decline ratio to assess market sentiment."""
        # Simulating real API call (Finnhub doesn’t provide this directly)
        advance_stocks = np.random.randint(2000, 3500)  # Example values
        decline_stocks = np.random.randint(1000, 3000)
        adv_dec_ratio = advance_stocks / max(1, decline_stocks)
        return {"advances": advance_stocks, "declines": decline_stocks, "ratio": round(adv_dec_ratio, 2)}

    async def fetch_sector_strength(self):
        """Fetches sector performance to identify strong/weak sectors."""
        sectors = ["Technology", "Financials", "Healthcare", "Energy", "Utilities", "Consumer Discretionary"]
        sector_scores = {sector: np.random.uniform(-3, 3) for sector in sectors}  # Simulating sector performance
        return sector_scores

    def analyze_market_conditions(self, adv_dec_ratio, sector_strength):
        """Determines if the market is in a bullish or risk-off state."""
        if adv_dec_ratio > 1.5:
            market_trend = "Bullish"
        elif adv_dec_ratio < 0.8:
            market_trend = "Bearish"
        else:
            market_trend = "Neutral"

        leading_sectors = [sec for sec, score in sector_strength.items() if score > 1]
        defensive_sectors = {"Utilities", "Healthcare"}

        if set(leading_sectors) & defensive_sectors:
            market_trend = "Risk-Off"

        return {"trend": market_trend, "leading_sectors": leading_sectors}

    async def get_market_breadth_summary(self):
        """Returns a summary of current market conditions."""
        adv_dec_data = await self.fetch_advance_decline_data()
        sector_strength = await self.fetch_sector_strength()
        market_analysis = self.analyze_market_conditions(adv_dec_data["ratio"], sector_strength)

        return {
            "adv_dec_data": adv_dec_data,
            "sector_strength": sector_strength,
            "market_trend": market_analysis["trend"],
            "leading_sectors": market_analysis["leading_sectors"],
        }

# Usage Example:
if __name__ == "__main__":
    async def test():
        finnhub = FinnhubClient("your_finnhub_api_key")
        market_breadth = MarketBreadth(finnhub)
        summary = await market_breadth.get_market_breadth_summary()
        print(summary)

    asyncio.run(test())

