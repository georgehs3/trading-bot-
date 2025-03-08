import datetime
import logging

import numpy as np
from transformers import pipeline


class NewsRanking:
    """Assigns a Trade Influence Score (0-100%) to financial news based on AI-driven analysis."""

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.time_decay_days = 7  # More recent news holds more weight
        self.high_risk_terms = [
            "SEC investigation",
            "lawsuit",
            "fraud",
            "regulatory action",
        ]
        self.credible_sources = {"Reuters", "Bloomberg", "CNBC", "WSJ"}

    def calculate_trade_influence_score(self, news_data):
        """Assigns a 0-100% Trade Influence Score based on sentiment, credibility, and historical impact."""
        if not news_data:
            return 0  # No news = No influence

        sentiment_scores = []
        for news in news_data:
            # AI Sentiment Analysis
            sentiment = self.sentiment_analyzer(news["headline"])[0]
            sentiment_strength = sentiment["score"]

            # Time Decay Function
            news_age = (datetime.datetime.utcnow() - news["date"]).days
            # Decays over a week
            recency_weight = max(0, 1 - (news_age / self.time_decay_days))

            # Source Credibility
            credibility_weight = 1.0 if news["source"] in self.credible_sources else 0.5

            # Historical Impact (earnings and major company news have stronger
            # influence)
            historical_impact = 0.8 if "earnings" in news["headline"].lower() else 0.5

            # High-Risk Event Filtering
            if any(term in news["headline"].lower() for term in self.high_risk_terms):
                self.logger.warning(f"Filtered high-risk news: {news['headline']}")
                continue  # Skip risky news items

            # Compute Trade Influence Score
            trade_score = sentiment_strength * recency_weight * credibility_weight * historical_impact * 100
            sentiment_scores.append(trade_score)

        return round(np.mean(sentiment_scores), 2) if sentiment_scores else 0


# Usage Example:
if __name__ == "__main__":
    config = {"news_ranking": {}}
    nr = NewsRanking(config)

    sample_news = [
        {
            "headline": "Company X reports record earnings growth",
            "source": "Bloomberg",
            "date": datetime.datetime.utcnow(),
        },
        {
            "headline": "SEC investigation launched into Company Y",
            "source": "Unknown",
            "date": datetime.datetime.utcnow(),
        },
    ]

    score = nr.calculate_trade_influence_score(sample_news)
    print(f"Trade Influence Score: {score}")
