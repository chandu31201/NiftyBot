import requests
import config


def _send(text: str):
    if "PASTE" in config.TELEGRAM_TOKEN:
        print(f"[Telegram] {text}")
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": config.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"},
            timeout=10,
        )
    except Exception as e:
        print(f"[Telegram] Error: {e}")


def bot_started(capital):
    mode = "📝 Paper Trading" if config.PAPER_TRADING else "💸 Live Trading"
    _send(
        f"🟢 <b>NiftyBot Started</b>\n"
        f"Mode: {mode}\n"
        f"Capital: ₹{capital:,.0f}\n"
        f"Max Loss/Day: ₹{config.MAX_LOSS_PER_DAY}"
    )


def bot_stopped(reason="Manual"):
    _send(f"🔴 <b>NiftyBot Stopped</b>\nReason: {reason}")


def trade_alert(action, price, qty, pnl=None):
    emoji = "🟢 BUY" if action == "BUY" else "🔴 SELL"
    msg   = f"{emoji} Nifty @ ₹{price:,.2f} | Qty: {qty}"
    if pnl is not None:
        msg += f"\nP&L this trade: ₹{pnl:+.2f}"
    _send(msg)


def daily_summary(total_trades, total_pnl, capital):
    emoji = "💰" if total_pnl >= 0 else "📉"
    _send(
        f"{emoji} <b>Daily Summary</b>\n"
        f"Trades: {total_trades}\n"
        f"P&L: ₹{total_pnl:+.2f}\n"
        f"Capital: ₹{capital:,.2f}"
    )
