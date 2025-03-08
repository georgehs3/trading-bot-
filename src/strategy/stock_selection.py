import logging
import asyncio
import numpy as np
from src.api.finnhub_client import FinnhubClient
from src.api.alpha_vantage_client import AlphaVantageClient
from src.database.db_connector import DatabaseConnector

class StockSelection:
    """Selects top 75 stocks dynamically based on liquidity, volatility, institutional flow, and sentiment analysis."""

    def __init__(self, finnhub: FinnhubClient, alpha_vantage: AlphaVantageClient, database: DatabaseConnector, config):
        self.finnhub = finnhub
        self.alpha_vantage = alpha_vantage
        self.database = database
        self.config = config["stock_selection"]
        self.logger = logging.getLogger(__name__)

    async def fetch_stock_data(self, stock_list):
        """Fetches real-time stock data and liquidity metrics."""
        tasks = [self.finnhub.get_stock_price(stock) for stock in stock_list]
        return await asyncio.gather(*tasks)

    async def fetch_sentiment_scores(self, stock_list):
        """Fetches sentiment scores for each stock."""
        return await self.alpha_vantage.get_news_sentiment(stock_list)

    def rank_stocks(self, stock_data, sentiment_data):
        """Ranks stocks based on multi-factor scoring."""
        scores = []
        for stock in stock_data:
            if not stock:
                continue

            # Scoring factors
            liquidity_score = stock["current_price"] * stock["previous_close"] * 0.3
            volatility_score = np.random.uniform(1, 3)  # Placeholder for ATR-based volatility
            sentiment_score = sentiment_data.get(stock["symbol"], 50)  # Default neutral sentiment

            institutional_flow = np.random.uniform(0, 100)  # Placeholder for dark pool/institutional flow
            total_score = (liquidity_score * 0.3) + (volatility_score * 0.2) + (sentiment_score * 0.3) + (institutional_flow * 0.2)

            scores.append((stock["symbol"], total_score))

        # Select top 75 stocks
        ranked_stocks = sorted(scores, key=lambda x: x[1], reverse=True)[:75]
        return [stock[0] for stock in ranked_stocks]

    async def update_stock_list(self):
        """Updates the tracked stock list dynamically."""
        all_stocks = self.database.get_tracked_stocks()

        stock_data = await self.fetch_stock_data(all_stocks)
        sentiment_data = await self.fetch_sentiment_scores(all_stocks)

        selected_stocks = self.rank_stocks(stock_data, sentiment_data)
        self.database.update_tracked_stocks(selected_stocks)

        self.logger.info(f"Updated tracked stocks: {selected_stocks}")

# Usage Example:
if __name__ == "__main__":
    async def test():
        config = {
            "stock_selection": {
                "liquidity_threshold": 1000000,
                "volatility_threshold": 2.0
            }
        }
        
        db = DatabaseConnector({"type": "postgresql", "connection_string": "postgresql://user:password@localhost/tradingbot"})
        finnhub = FinnhubClient("your_finnhub_api_key")
        alpha_vantage = AlphaVantageClient("your_alpha_vantage_api_key")
        stock_selector = StockSelection(finnhub, alpha_vantage, db, config)
        
        await stock_selector.update_stock_list()

    asyncio.run(test())

