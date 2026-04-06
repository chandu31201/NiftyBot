import yfinance as yf
import pandas as pd
from datetime import datetime


def get_nifty_data(period="5d", interval="5m"):
    try:
        df = yf.Ticker("^NSEI").history(period=period, interval=interval)
        if df.empty:
            return None
        return df[["Open", "High", "Low", "Close", "Volume"]]
    except Exception as e:
        print(f"[Scanner] Data error: {e}")
        return None


def get_current_price():
    try:
        data = yf.Ticker("^NSEI").history(period="1d", interval="1m")
        if data.empty:
            return None
        return round(float(data["Close"].iloc[-1]), 2)
    except Exception as e:
        print(f"[Scanner] Price error: {e}")
        return None


def get_vix():
    try:
        data = yf.Ticker("^INDIAVIX").history(period="1d", interval="1m")
        if data.empty:
            return None
        return round(float(data["Close"].iloc[-1]), 2)
    except:
        return None


def get_market_status():
    now = datetime.now()
    if now.weekday() >= 5:
        return False, "Weekend — Market Closed 🔴"
    open_t  = now.replace(hour=9,  minute=15, second=0, microsecond=0)
    close_t = now.replace(hour=15, minute=15, second=0, microsecond=0)
    if open_t <= now <= close_t:
        return True, "Market Open 🟢"
    elif now < open_t:
        mins = int((open_t - now).total_seconds() // 60)
        return False, f"Opens in {mins} min ⏳"
    else:
        return False, "Market Closed 🔴"


def calculate_ema(df, period):
    return df["Close"].ewm(span=period, adjust=False).mean()
