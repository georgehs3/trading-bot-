from flask import Flask, render_template, jsonify
import logging
import os
from src.database.db_connector import DatabaseConnector

app = Flask(__name__)

# Load database config
db_config = {
    "type": "postgresql",
    "connection_string": os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost/tradingbot",
    ),
}
database = DatabaseConnector(db_config)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def index():
    """Renders the main dashboard UI."""
    return render_template("index.html")


@app.route("/trade-metrics")
def trade_metrics():
    """Fetches trade performance metrics from the database."""
    try:
        query = """
            SELECT COUNT(*) AS total_trades,
                SUM(CASE WHEN exit_price > entry_price THEN 1 ELSE 0 END)
                    AS winning_trades,
                SUM(CASE WHEN exit_price <= entry_price THEN 1 ELSE 0 END)
                    AS losing_trades,
                ROUND(AVG(exit_price - entry_price), 2) AS avg_profit
            FROM trade_logs;
        """
        conn = database.conn
        with conn.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchone()
            metrics = {
                "total_trades": data[0],
                "win_rate": round((data[1] / data[0]) * 100, 2) if data[0] > 0 else 0,
                "avg_profit": data[3] if data[3] else 0,
            }
        return jsonify(metrics)
    except Exception as e:
        logger.error(f"Error fetching trade metrics: {e}")
        return jsonify({"error": "Failed to retrieve trade metrics"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
