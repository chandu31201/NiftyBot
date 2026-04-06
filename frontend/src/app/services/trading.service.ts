import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class TradingService {
  private ws!: WebSocket;
  public messages$ = new Subject<any>();

  constructor(private http: HttpClient) {
    this.connect();
  }

  private connect() {
    const proto = location.protocol === 'https:' ? 'wss' : 'ws';
    this.ws = new WebSocket(`${proto}://${location.host}/ws`);
    this.ws.onmessage = (e) => this.messages$.next(JSON.parse(e.data));
    this.ws.onclose   = ()  => setTimeout(() => this.connect(), 3000);
    this.ws.onerror   = ()  => this.ws.close();
  }

  getStatus()    { return this.http.get<any>('/api/status'); }
  getTrades()    { return this.http.get<any>('/api/trades'); }
  getStats()     { return this.http.get<any>('/api/stats'); }
  startBot()     { return this.http.post<any>('/api/bot/start', {}); }
  stopBot()      { return this.http.post<any>('/api/bot/stop', {}); }
}
