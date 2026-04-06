# ============================================================
#   NIFTY BOT - YOUR SETTINGS
#   Fill in your details below. That's all you need to do.
# ============================================================

# --- TELEGRAM SETTINGS ---
TELEGRAM_TOKEN   = "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "PASTE_YOUR_CHAT_ID_HERE"

# --- GROWW API (leave blank for paper trading) ---
GROWW_API_KEY    = ""
GROWW_SECRET_KEY = ""

# --- TRADING SETTINGS ---
PAPER_TRADING    = True        # Set to False only when ready for real money
STARTING_CAPITAL = 50000       # Virtual money for paper trading (₹)
MAX_LOSS_PER_DAY = 500         # Bot stops if loss exceeds this (₹)
MAX_POSITIONS    = 3           # Max open trades at once
TRADE_AMOUNT     = 2000        # Amount per trade (₹)

# --- STRATEGY SETTINGS ---
EMA_FAST         = 9           # Fast EMA period
EMA_SLOW         = 21          # Slow EMA period
SCAN_INTERVAL    = 120         # Scan every 120 seconds (2 mins)

# --- MARKET HOURS (IST) ---
MARKET_OPEN      = "09:15"
MARKET_CLOSE     = "15:15"
