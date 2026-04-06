from bot.scanner import get_nifty_data, calculate_ema
import config

def check_signal():
    """
    EMA Crossover Strategy:
    BUY  signal → Fast EMA crosses ABOVE Slow EMA
    SELL signal → Fast EMA crosses BELOW Slow EMA
    Returns: 'BUY', 'SELL', or 'HOLD'
    """
    df = get_nifty_data(period="5d", interval="5m")
    if df is None or len(df) < config.EMA_SLOW + 5:
        return "HOLD", None, None

    ema_fast = calculate_ema(df, config.EMA_FAST)
    ema_slow = calculate_ema(df, config.EMA_SLOW)

    current_price = round(float(df['Close'].iloc[-1]), 2)

    # Previous candle values
    prev_fast = ema_fast.iloc[-2]
    prev_slow = ema_slow.iloc[-2]
    curr_fast = ema_fast.iloc[-1]
    curr_slow = ema_slow.iloc[-1]

    # Crossover detection
    bullish_cross = (prev_fast <= prev_slow) and (curr_fast > curr_slow)
    bearish_cross = (prev_fast >= prev_slow) and (curr_fast < curr_slow)

    ema_values = {
        "ema_fast": round(curr_fast, 2),
        "ema_slow": round(curr_slow, 2),
        "trend": "Bullish 📈" if curr_fast > curr_slow else "Bearish 📉"
    }

    if bullish_cross:
        return "BUY", current_price, ema_values
    elif bearish_cross:
        return "SELL", current_price, ema_values
    else:
        return "HOLD", current_price, ema_values
