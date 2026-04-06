from bot.scanner import get_nifty_data, calculate_ema
import config


def check_signal():
    """
    Returns: signal ('BUY'/'SELL'/'HOLD'), price, ema_info dict
    """
    df = get_nifty_data()
    if df is None or len(df) < config.EMA_SLOW + 5:
        return "HOLD", None, {}

    ema_fast = calculate_ema(df, config.EMA_FAST)
    ema_slow = calculate_ema(df, config.EMA_SLOW)
    price    = round(float(df["Close"].iloc[-1]), 2)

    pf, ps = ema_fast.iloc[-2], ema_slow.iloc[-2]
    cf, cs = ema_fast.iloc[-1], ema_slow.iloc[-1]

    ema_info = {
        "ema_fast": round(cf, 2),
        "ema_slow": round(cs, 2),
        "trend": "Bullish 📈" if cf > cs else "Bearish 📉",
    }

    if pf <= ps and cf > cs:
        return "BUY", price, ema_info
    elif pf >= ps and cf < cs:
        return "SELL", price, ema_info
    return "HOLD", price, ema_info
