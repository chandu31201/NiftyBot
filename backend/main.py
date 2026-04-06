import asyncio
import json
import threading
import time
from datetime import datetime
from typing import List

import config
from bot.scanner   import get_current_price, get_market_status, get_vix
from bot.strategy  import check_signal
from bot.trader    import PaperTrader
from bot           import telegram_alerts as tg

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="NiftyBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

trader   = PaperTrader()
clients: List[WebSocket] = []
price_cache = {"price": None, "vix": None, "market": "Checking..."}


# ── WebSocket broadcast ────────────────────────────────────────────────────────
async def broadcast(data: dict):
    dead = []
    for ws in clients:
        try:
            await ws.send_json(data)
        except:
            dead.append(ws)
    for ws in dead:
        clients.remove(ws)


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    try:
        while True:
            await ws.receive_text()   # keep alive
    except WebSocketDisconnect:
        clients.remove(ws)


# ── Background price poller ────────────────────────────────────────────────────
def price_loop():
    loop = asyncio.new_event_loop()
    while True:
        try:
            price = get_current_price()
            vix   = get_vix()
            _, market_msg = get_market_status()
            price_cache.update({"price": price, "vix": vix, "market": market_msg})

            payload = {
                "type":    "price",
                "price":   price,
                "vix":     vix,
                "market":  market_msg,
                "time":    datetime.now().strftime("%H:%M:%S"),
                **trader.get_stats(),
            }
            loop.run_until_complete(broadcast(payload))
        except Exception as e:
            print(f"[PriceLoop] {e}")
        time.sleep(5)


# ── Bot scan loop ──────────────────────────────────────────────────────────────
def bot_loop():
    loop = asyncio.new_event_loop()
    while True:
        if trader.running:
            is_open, _ = get_market_status()
            if is_open:
                try:
                    signal, price, ema_info = check_signal()
                    trader.status_msg = f"Last scan: {signal} @ {datetime.now().strftime('%H:%M:%S')}"
                    if signal in ("BUY", "SELL") and price:
                        trade = trader.execute(signal, price)
                        if trade:
                            payload = {
                                "type":  "trade",
                                "trade": trade,
                                **trader.get_stats(),
                            }
                            loop.run_until_complete(broadcast(payload))
                except Exception as e:
                    print(f"[BotLoop] {e}")
        time.sleep(config.SCAN_INTERVAL)


threading.Thread(target=price_loop, daemon=True).start()
threading.Thread(target=bot_loop,   daemon=True).start()


# ── REST endpoints ─────────────────────────────────────────────────────────────
@app.get("/api/status")
def get_status():
    _, market_msg = get_market_status()
    return {
        **trader.get_stats(),
        "market":  market_msg,
        "price":   price_cache["price"],
        "vix":     price_cache["vix"],
        "mode":    "Paper Trading" if config.PAPER_TRADING else "Live Trading",
    }


@app.post("/api/bot/start")
def start_bot():
    if not trader.running:
        trader.running    = True
        trader.status_msg = "Running 🟢"
        tg.bot_started(trader.capital)
    return {"success": True, "message": "Bot started"}


@app.post("/api/bot/stop")
def stop_bot():
    if trader.running:
        trader.running    = False
        trader.status_msg = "Stopped 🔴"
        tg.bot_stopped("Manual stop")
    return {"success": True, "message": "Bot stopped"}


@app.get("/api/trades")
def get_trades():
    return {"trades": list(reversed(trader.trades[-50:]))}


@app.get("/api/stats")
def get_stats():
    stats = trader.get_stats()
    wins  = [t for t in trader.trades if t.get("pnl", 0) > 0]
    loss  = [t for t in trader.trades if t.get("pnl", 0) < 0]
    stats["win_rate"] = (
        round(len(wins) / (len(wins) + len(loss)) * 100, 1)
        if (wins or loss) else 0
    )
    return stats
