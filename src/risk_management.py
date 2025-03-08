import logging
import numpy as np

class RiskManagement:
    """Handles ATR-based stop-loss, position sizing, and adaptive risk allocation."""

    def __init__(self, config):
        self.base_risk_per_trade = config["trading"]["position_sizing"]["base_risk_per_trade"]
        self.atr_multiplier = config["trading"]["stop_loss_atr_multiplier"]
        self.adaptive_risk = config["trading"]["position_sizing"]["adaptive_risk"]
        self.logger = logging.getLogger(__name__)

    def calculate_stop_loss(self, atr, current_price):
        """Calculates dynamic stop-loss using ATR multiplier."""
        stop_loss = round(current_price - (atr * self.atr_multiplier), 2)
        return max(0, stop_loss)  # Ensure stop-loss is positive

    def calculate_position_size(self, account_balance, atr, stock_price, confidence_score):
        """Determines optimal position size based on confidence score and ATR."""
        risk_allocation = self.base_risk_per_trade
        if self.adaptive_risk:
            risk_allocation *= (confidence_score / 100)  # Higher confidence = larger position

        risk_per_share = atr * self.atr_multiplier
        position_size = (account_balance * risk_allocation) / risk_per_share
        return max(1, int(position_size))  # Minimum position size is 1 share

    def apply_trailing_stop(self, current_price, entry_price, atr):
        """Implements ATR-based trailing stop-loss strategy."""
        trailing_stop = round(entry_price + (atr * 1.5), 2)  # 1.5x ATR trailing stop
        return max(trailing_stop, current_price)

    def adjust_risk_on_high_volatility(self, market_volatility):
        """Reduces risk exposure on high-volatility days."""
        if market_volatility > 3.0:  # Example threshold for high-risk days
            return self.base_risk_per_trade * 0.5  # Reduce risk exposure
        return self.base_risk_per_trade

# Usage Example:
if __name__ == "__main__":
    config = {
        "trading": {
            "position_sizing": {"base_risk_per_trade": 0.02, "adaptive_risk": True},
            "stop_loss_atr_multiplier": 2.0
        }
    }
    
    rm = RiskManagement(config)
    print(rm.calculate_stop_loss(atr=1.5, current_price=100))
    print(rm.calculate_position_size(account_balance=10000, atr=1.5, stock_price=100, confidence_score=80))

