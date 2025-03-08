-- PostgreSQL schema setup for trading bot

-- Table to store executed trades
CREATE TABLE IF NOT EXISTS trade_logs (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    action VARCHAR(10) CHECK (action IN ('BUY', 'SELL')) NOT NULL,
    entry_price NUMERIC(10,2) NOT NULL,
    exit_price NUMERIC(10,2),
    stop_loss NUMERIC(10,2) NOT NULL,
    take_profit NUMERIC(10,2),
    confidence_score NUMERIC(5,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store stock selection & tracking
CREATE TABLE IF NOT EXISTS tracked_stocks (
    symbol VARCHAR(10) PRIMARY KEY,
    liquidity_score NUMERIC(10,2),
    volatility_score NUMERIC(10,2),
    sentiment_score NUMERIC(10,2),
    institutional_flow NUMERIC(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for market sentiment & trend signals
CREATE TABLE IF NOT EXISTS market_signals (
    id SERIAL PRIMARY KEY,
    market_trend VARCHAR(15) CHECK (market_trend IN ('Bullish', 'Bearish', 'Neutral')) NOT NULL,
    advance_decline_ratio NUMERIC(5,2),
    sector_strength JSONB,
    institutional_activity JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance optimization
CREATE INDEX idx_trade_symbol ON trade_logs(symbol);
CREATE INDEX idx_market_trend ON market_signals(market_trend);
CREATE INDEX idx_tracked_stocks_updated ON tracked_stocks(last_updated);

