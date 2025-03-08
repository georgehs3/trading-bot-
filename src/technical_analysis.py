import logging

import numpy as np
import torch
import torch.nn as nn


class CNNPatternRecognition(nn.Module):
    """CNN model for recognizing candlestick patterns in stock charts."""

    def __init__(self):
        super(CNNPatternRecognition, self).__init__()
        self.conv1 = nn.Conv1d(
            in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1
        )
        self.conv2 = nn.Conv1d(
            in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1
        )
        self.fc1 = nn.Linear(32 * 50, 128)
        self.fc2 = nn.Linear(128, 3)  # 3 categories: Bullish, Neutral, Bearish

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class TechnicalAnalysis:
    """Uses AI for candlestick pattern recognition and trend prediction."""

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.model = CNNPatternRecognition()
        self.model.load_state_dict(
            torch.load(config["ai"]["model_path"])
        )  # Load trained model
        self.model.eval()

    def predict_pattern(self, historical_data):
        """Predicts if a stock is in a bullish, neutral, or bearish pattern."""
        data_tensor = (
            torch.tensor(historical_data, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        )  # Reshape for CNN
        output = self.model(data_tensor)
        prediction = torch.argmax(output, dim=1).item()
        return ["Bullish", "Neutral", "Bearish"][prediction]

    def analyze_stock(self, stock_data):
        """Runs AI-based pattern recognition on stock price history."""
        if len(stock_data) < 50:
            self.logger.warning("Not enough data for pattern recognition.")
            return "Insufficient Data"

        return self.predict_pattern(stock_data)


# Usage Example:
if __name__ == "__main__":
    config = {"ai": {"model_path": "src/models/cnn_model.pth"}}

    ta = TechnicalAnalysis(config)
    sample_data = np.random.randn(50)  # Simulated 50-period stock price data
    prediction = ta.analyze_stock(sample_data)
    print(f"Predicted Market Pattern: {prediction}")
