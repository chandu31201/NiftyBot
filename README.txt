====================================================
  NIFTYBOT — SETUP GUIDE
  Read this fully before starting. Takes 20 mins.
====================================================

WHAT THIS BOT DOES
------------------
- Watches Nifty 50 live price every 2 minutes
- Detects buy/sell signals using EMA crossover strategy
- Trades automatically (paper money by default — safe)
- Sends every trade alert to your Telegram
- Shows everything on a live dashboard in your browser


BEFORE YOU START — INSTALL THESE TWO THINGS
--------------------------------------------
1. Python  → python.org/downloads
   ⚠️  During install, TICK "Add Python to PATH"

2. Node.js → nodejs.org
   Download the LTS version, install with defaults


STEP 1 — FILL YOUR DETAILS
----------------------------
Open the file:  backend/config.py

Fill these 4 lines (keep the quotes):

  TELEGRAM_TOKEN    = "your telegram token here"
  TELEGRAM_CHAT_ID  = "your chat ID here"
  GROWW_API_KEY     = ""   ← leave blank for paper trading
  GROWW_SECRET_KEY  = ""   ← leave blank for paper trading

How to get Telegram Token:
  - Open Telegram → search @BotFather → /newbot → copy token

How to get Chat ID:
  - Open Telegram → search @userinfobot → press Start → copy the number

Save the file.


STEP 2 — START THE BOT
------------------------
Double-click:  run.bat

It will:
  ✅ Install everything automatically
  ✅ Start the backend server
  ✅ Start the dashboard
  ✅ Open your browser at http://localhost:4200


STEP 3 — USE THE DASHBOARD
----------------------------
  - Press "▶ Start Bot" button to begin
  - Bot scans Nifty every 2 minutes
  - Every trade appears in Trade History table
  - Every trade sends a Telegram message to your phone
  - Daily P&L shows how much you made/lost today


STEP 4 — PAPER TRADING FIRST (VERY IMPORTANT)
-----------------------------------------------
By default PAPER_TRADING = True in config.py
This means it uses FAKE money (₹50,000 virtual)

DO NOT change this to False until:
  ✓ Bot runs for 2 full weeks
  ✓ You are consistently making ₹500–1000/day on paper
  ✓ You understand why each trade was made


DAILY LOSS PROTECTION
----------------------
Bot auto-stops if you lose ₹500 in one day.
Change MAX_LOSS_PER_DAY in config.py to adjust.


FOLDERS EXPLAINED
------------------
  backend/          → FastAPI server + bot logic
  backend/config.py → YOUR SETTINGS (only file you touch)
  frontend/         → Angular dashboard (don't touch)
  run.bat           → Double-click to start everything


SUPPORT
-------
If something breaks, screenshot the error and ask for help.
API docs available at: http://localhost:8000/docs

====================================================
  START PAPER TRADING. BE PATIENT. SCALE SLOWLY.
====================================================
