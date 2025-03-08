import logging
import requests


class DiscordBot:
    """Handles real-time trade alerts via Discord."""

    def __init__(self, webhook_url):
        self.logger = logging.getLogger(__name__)
        self.webhook_url = webhook_url

    def send_trade_alert(self, trade_signal):
        """Sends a trade alert message to Discord using embeds."""
        embed = {
            "title": f"📈 Trade Alert: {trade_signal['symbol']}",
            "color": 3066993,  # Green color for positive sentiment
            "fields": [
                {"name": "🎯 Action", "value": trade_signal["action"], "inline": True},
                {
                    "name": "📌 Entry Range",
                    "value": f"{trade_signal['entry_range'][0]:.2f} - {trade_signal['entry_range'][1]:.2f}",
                    "inline": True,
                },
                {
                    "name": "🚨 Stop Loss",
                    "value": f"{trade_signal['stop_loss']:.2f}",
                    "inline": True,
                },
                {
                    "name": "💰 Take Profit",
                    "value": f"{trade_signal['take_profit']:.2f}",
                    "inline": True,
                },
                {
                    "name": "📊 Confidence Score",
                    "value": f"{trade_signal['confidence']}%",
                    "inline": True,
                },
            ],
            "footer": {"text": "#StockMarket #TradingBot"},
        }
        return self._send_message({"embeds": [embed]})

    def send_general_alert(self, message):
        """Sends a general system alert to Discord."""
        return self._send_message({"content": f"⚠️ {message}"})

    def _send_message(self, data):
        """Handles sending messages to Discord via Webhooks."""
        try:
            response = requests.post(self.webhook_url, json=data)
            if response.status_code == 204:
                self.logger.info("Discord alert sent successfully.")
                return True
            self.logger.error(f"Discord API error: {response.text}")
        except Exception as e:
            self.logger.error(f"Failed to send Discord alert: {e}")
        return False


# Usage Example:
if __name__ == "__main__":
    discord_bot = DiscordBot(webhook_url="your_discord_webhook_url")
    sample_trade_signal = {
        "symbol": "TSLA",
        "action": "BUY",
        "entry_range": (800.00, 805.00),
        "stop_loss": 790.00,
        "take_profit": 825.00,
        "confidence": 90,
    }
    discord_bot.send_trade_alert(sample_trade_signal)
