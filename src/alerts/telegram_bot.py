import logging
import requests

class TelegramBot:
    """Handles real-time trade alerts via Telegram."""

    def __init__(self, bot_token, chat_id):
        self.logger = logging.getLogger(__name__)
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_trade_alert(self, trade_signal):
        """Sends a trade alert message with detailed trade insights."""
        message = (
            f"📈 *Trade Alert: {trade_signal['symbol']}*\n"
            f"🎯 *Action:* {trade_signal['action']}\n"
            f"📌 *Entry Range:* {trade_signal['entry_range'][0]:.2f} - {trade_signal['entry_range'][1]:.2f}\n"
            f"🚨 *Stop Loss:* {trade_signal['stop_loss']:.2f}\n"
            f"💰 *Take Profit:* {trade_signal['take_profit']:.2f}\n"
            f"📊 *Confidence Score:* {trade_signal['confidence']}%\n"
            f"#StockMarket #TradingBot"
        )
        return self._send_message(message)

    def send_general_alert(self, message):
        """Sends a general update or system alert to Telegram."""
        return self._send_message(f"⚠️ {message}")

    def _send_message(self, message):
        """Handles sending messages to Telegram."""
        try:
            response = requests.post(self.api_url, json={"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"})
            if response.status_code == 200:
                self.logger.info("Telegram alert sent successfully.")
                return True
            else:
                self.logger.error(f"Telegram API error: {response.text}")
        except Exception as e:
            self.logger.error(f"Failed to send Telegram alert: {e}")
        return False

# Usage Example:
if __name__ == "__main__":
    telegram_bot = TelegramBot(bot_token="your_telegram_bot_token", chat_id="your_chat_id")

    sample_trade_signal = {
        "symbol": "AAPL",
        "action": "BUY",
        "entry_range": (345.00, 348.00),
        "stop_loss": 340.00,
        "take_profit": 360.00,
        "confidence": 85
    }

    telegram_bot.send_trade_alert(sample_trade_signal)

