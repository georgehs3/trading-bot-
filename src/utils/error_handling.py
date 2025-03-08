import logging
import time
import traceback

import requests


class ErrorHandling:
    """Handles system errors, API failures, and fallback mechanisms."""

    def __init__(self, telegram_bot_token=None, telegram_chat_id=None):
        self.logger = logging.getLogger(__name__)
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id

    def send_alert(self, message):
        """Sends critical error alerts via Telegram."""
        if self.telegram_bot_token and self.telegram_chat_id:
            try:
                url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
                data = {
                    "chat_id": self.telegram_chat_id,
                    "text": message,
                    "parse_mode": "Markdown",
                }
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    self.logger.info("Telegram alert sent successfully.")
                else:
                    self.logger.error(f"Failed to send Telegram alert: {response.text}")
            except Exception as e:
                self.logger.error(f"Telegram alert error: {e}")

    def retry_operation(self, func, retries=3, delay=2):
        """Retries a failed operation with exponential backoff."""
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(delay * (2**attempt))  # Exponential backoff
        self.logger.error("Operation failed after maximum retries.")
        return None

    def handle_critical_failure(self, error_message, exception_obj=None):
        """Handles critical failures by logging, alerting, and triggering failover."""
        error_details = f"CRITICAL ERROR: {error_message}\n"
        if exception_obj:
            error_details += f"Exception: {str(exception_obj)}\n"
            error_details += "".join(traceback.format_exception(None, exception_obj, exception_obj.__traceback__))

        self.logger.critical(error_details)
        self.send_alert(error_details)


# Usage Example:
if __name__ == "__main__":
    error_handler = ErrorHandling(telegram_bot_token="your_telegram_bot_token", telegram_chat_id="your_chat_id")

    # Example: Retry a failing function
    def sample_failing_function():
        raise Exception("API Error")

    result = error_handler.retry_operation(sample_failing_function)
    print(f"Final result: {result}")

    # Example: Trigger a critical failure alert
    try:
        raise ValueError("Simulated critical system failure")
    except Exception as e:
        error_handler.handle_critical_failure("System Crash Detected!", e)
