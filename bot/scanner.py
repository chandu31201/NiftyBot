import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_nifty_data(period="5d", interval="5m"):
    """Fetch real Nifty 50 data from Yahoo Finance (free)"""
    try:
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(period=period, interval=interval)
        if df.empty:
            return None
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        print(f"[Scanner] Error fetching data: {e}")
        return None

def get_current_price():
    """Get current Nifty 50 price"""
    try:
        ticker = yf.Ticker("^NSEI")
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            return None
        return round(float(data['Close'].iloc[-1]), 2)
    except Exception as e:
        print(f"[Scanner] Error getting price: {e}")
        return None

def calculate_ema(df, period):
    """Calculate Exponential Moving Average"""
    return df['Close'].ewm(span=period, adjust=False).mean()

def get_market_status():
    """Check if Indian market is open"""
    now = datetime.now()
    # Monday=0 to Friday=4
    if now.weekday() >= 5:
        return False, "Weekend - Market Closed"
    market_open  = now.replace(hour=9,  minute=15, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=15, second=0, microsecond=0)
    if market_open <= now <= market_close:
        return True, "Market Open 🟢"
    elif now < market_open:
        opens_in = market_open - now
        mins = int(opens_in.total_seconds() // 60)
        return False, f"Opens in {mins} mins"
    else:
        return False, "Market Closed 🔴"

def get_vix():
    """Get India VIX"""
    try:
        vix = yf.Ticker("^INDIAVIX")
        data = vix.history(period="1d", interval="1m")
        if data.empty:
            return None
        return round(float(data['Close'].iloc[-1]), 2)
    except:
        return None
