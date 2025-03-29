import requests
import pandas as pd
from telegram import Bot
import time

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"  # Replace with your Telegram chat ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Function to send alerts to Telegram
def send_alert(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Function to simulate fetching market data (Replace with real data source)
def fetch_market_data():
    # Replace this with actual Pocket Option data (scraping/API if available)
    market_data = {
        "current_price": 1.1850,
        "ema_7": 1.1850,
        "ema_14": 1.1860,
        "stochastic_k": 20,
        "stochastic_d": 22,
        "accelerator": 0.0001,
        "rsi": 35,
        "support": 1.1830,  # Example Support Level
        "resistance": 1.1880,  # Example Resistance Level
        "previous_candle": {"open": 1.1845, "close": 1.1855, "high": 1.1865, "low": 1.1835},  # Example Candlestick
    }
    return market_data

# Function to check price action signals
def analyze_price_action(data):
    price = data["current_price"]
    support = data["support"]
    resistance = data["resistance"]
    prev_candle = data["previous_candle"]

    # Support Bounce (Bullish Signal)
    if price <= support and prev_candle["close"] > prev_candle["open"]:
        return "📈 Price Rejected Support - Possible Buy"

    # Resistance Rejection (Bearish Signal)
    if price >= resistance and prev_candle["close"] < prev_candle["open"]:
        return "📉 Price Rejected Resistance - Possible Sell"

    return None  # No strong price action signal

# Function to analyze market conditions and send alerts
def analyze_market():
    data = fetch_market_data()

    # EMA Crossover
    ema_buy = data["ema_7"] > data["ema_14"]
    ema_sell = data["ema_7"] < data["ema_14"]

    # Stochastic Confirmation
    stochastic_buy = data["stochastic_k"] > data["stochastic_d"] and data["stochastic_k"] < 20  # Oversold
    stochastic_sell = data["stochastic_k"] < data["stochastic_d"] and data["stochastic_k"] > 80  # Overbought

    # Accelerator Confirmation
    accelerator_buy = data["accelerator"] > 0
    accelerator_sell = data["accelerator"] < 0

    # RSI Confirmation
    rsi_buy = data["rsi"] < 30  # Oversold
    rsi_sell = data["rsi"] > 70  # Overbought

    # Check Price Action
    price_action_signal = analyze_price_action(data)

    # Generate Trade Alerts
    if ema_buy and stochastic_buy and accelerator_buy and rsi_buy:
        send_alert("📈 STRONG BUY SIGNAL - EMA, Stochastic, Accelerator & RSI Confirmed")

    elif ema_sell and stochastic_sell and accelerator_sell and rsi_sell:
        send_alert("📉 STRONG SELL SIGNAL - EMA, Stochastic, Accelerator & RSI Confirmed")

    elif price_action_signal:
        send_alert(price_action_signal)  # Send price action-based alert

# Run market analysis every minute (use scheduler for continuous execution)
while True:
    analyze_market()
    time.sleep(60)  # Wait for 1 minute before checking again
