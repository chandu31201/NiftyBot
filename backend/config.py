# ============================================================
#   NIFTY BOT — YOUR SETTINGS
#   Only fill the 4 lines below. Nothing else to change.
# ============================================================

TELEGRAM_TOKEN    = "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID  = "PASTE_YOUR_CHAT_ID_HERE"

GROWW_API_KEY     = ""   # Leave blank for paper trading
GROWW_SECRET_KEY  = ""   # Leave blank for paper trading

# ---- TRADING RULES ----
PAPER_TRADING     = True     # Change to False only for real money
STARTING_CAPITAL  = 50000    # Virtual capital in ₹
MAX_LOSS_PER_DAY  = 500      # Bot stops if daily loss exceeds this
MAX_POSITIONS     = 3
TRADE_AMOUNT      = 2000

# ---- STRATEGY ----
EMA_FAST          = 9
EMA_SLOW          = 21
SCAN_INTERVAL     = 120      # seconds between each scan

# ---- MARKET HOURS IST ----
MARKET_OPEN       = "09:15"
MARKET_CLOSE      = "15:15"
