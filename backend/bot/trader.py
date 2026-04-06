from datetime import datetime
from typing import List, Dict
import config
from bot import telegram_alerts as tg


class PaperTrader:
    def __init__(self):
        self.capital       = config.STARTING_CAPITAL
        self.daily_pnl     = 0.0
        self.total_pnl     = 0.0
        self.trades: List[Dict] = []
        self.open_position = None
        self.running       = False
        self.status_msg    = "Idle"
        self.today         = datetime.now().date()

    def reset_daily(self):
        if datetime.now().date() != self.today:
            self.daily_pnl = 0.0
            self.today     = datetime.now().date()

    def can_trade(self):
        self.reset_daily()
        if self.daily_pnl <= -config.MAX_LOSS_PER_DAY:
            self.running    = False
            self.status_msg = "Daily loss limit hit — stopped"
            tg.bot_stopped("Daily loss limit hit")
            return False
        if self.open_position and len([t for t in self.trades if t["status"] == "OPEN"]) >= config.MAX_POSITIONS:
            return False
        return True

    def execute(self, signal: str, price: float):
        if not self.can_trade():
            return None

        qty = int(config.TRADE_AMOUNT / price)
        if qty == 0:
            return None

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if signal == "BUY" and self.open_position is None:
            self.open_position = {"price": price, "qty": qty, "time": now}
            trade = {
                "id":     len(self.trades) + 1,
                "time":   now,
                "action": "BUY",
                "price":  price,
                "qty":    qty,
                "pnl":    0.0,
                "status": "OPEN",
            }
            self.trades.append(trade)
            tg.trade_alert("BUY", price, qty)
            return trade

        if signal == "SELL" and self.open_position is not None:
            entry = self.open_position
            pnl   = (price - entry["price"]) * entry["qty"]
            self.daily_pnl     += pnl
            self.total_pnl     += pnl
            self.capital       += pnl
            self.open_position  = None

            # Close previous open trade
            for t in reversed(self.trades):
                if t["status"] == "OPEN":
                    t["status"] = "CLOSED"
                    t["pnl"]    = round(pnl, 2)
                    break

            trade = {
                "id":     len(self.trades) + 1,
                "time":   now,
                "action": "SELL",
                "price":  price,
                "qty":    entry["qty"],
                "pnl":    round(pnl, 2),
                "status": "CLOSED",
            }
            self.trades.append(trade)
            tg.trade_alert("SELL", price, entry["qty"], pnl)
            return trade

        return None

    def get_stats(self):
        return {
            "capital":      round(self.capital, 2),
            "daily_pnl":    round(self.daily_pnl, 2),
            "total_pnl":    round(self.total_pnl, 2),
            "total_trades": len([t for t in self.trades if t["action"] == "BUY"]),
            "open_position": self.open_position,
            "running":      self.running,
            "status_msg":   self.status_msg,
        }
