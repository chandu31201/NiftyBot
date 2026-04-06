import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TradingService } from '../services/trading.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls:   ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, OnDestroy {
  price      = 0;
  vix        = 0;
  market     = 'Checking...';
  capital    = 0;
  dailyPnl   = 0;
  totalPnl   = 0;
  totalTrades= 0;
  winRate    = 0;
  botRunning = false;
  statusMsg  = 'Idle';
  mode       = 'Paper Trading';
  trades: any[] = [];
  priceHistory: number[] = [];
  lastUpdate = '';

  private sub!: Subscription;

  constructor(private svc: TradingService) {}

  ngOnInit() {
    // Load initial data
    this.svc.getStatus().subscribe(d => this.applyData(d));
    this.svc.getTrades().subscribe(d => this.trades = d.trades);
    this.svc.getStats().subscribe(d => { this.winRate = d.win_rate; });

    // Live WebSocket updates
    this.sub = this.svc.messages$.subscribe(msg => {
      if (msg.type === 'price') {
        this.price      = msg.price  ?? this.price;
        this.vix        = msg.vix    ?? this.vix;
        this.market     = msg.market ?? this.market;
        this.lastUpdate = msg.time;
        this.applyStats(msg);
        if (msg.price) {
          this.priceHistory.push(msg.price);
          if (this.priceHistory.length > 60) this.priceHistory.shift();
        }
      }
      if (msg.type === 'trade') {
        this.svc.getTrades().subscribe(d => this.trades = d.trades);
        this.applyStats(msg);
      }
    });
  }

  applyData(d: any) {
    this.price      = d.price      ?? 0;
    this.vix        = d.vix        ?? 0;
    this.market     = d.market     ?? '';
    this.mode       = d.mode       ?? '';
    this.applyStats(d);
  }

  applyStats(d: any) {
    this.capital     = d.capital      ?? this.capital;
    this.dailyPnl    = d.daily_pnl    ?? this.dailyPnl;
    this.totalPnl    = d.total_pnl    ?? this.totalPnl;
    this.totalTrades = d.total_trades ?? this.totalTrades;
    this.botRunning  = d.running      ?? this.botRunning;
    this.statusMsg   = d.status_msg   ?? this.statusMsg;
  }

  toggleBot() {
    if (this.botRunning) {
      this.svc.stopBot().subscribe(() => this.botRunning = false);
    } else {
      this.svc.startBot().subscribe(() => this.botRunning = true);
    }
  }

  pnlClass(pnl: number) {
    return pnl >= 0 ? 'positive' : 'negative';
  }

  ngOnDestroy() { this.sub?.unsubscribe(); }
}
