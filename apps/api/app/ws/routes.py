from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
import asyncio
import json
import websockets
import httpx
import random

router = APIRouter()

# Кэш Бинанса, чтоб не ддосить их апишку на каждом чихе
BINANCE_CACHE = {}

async def yahoo_finance_proxy(websocket: WebSocket, symbols: list[str]):
    # Яху Финанс для дедовских акций (AAPL, TSLA и прочий нормисовский скам)
    try:
        async with httpx.AsyncClient() as client:
            while True:
                ticks = []
                for sym in symbols:
                    try:
                        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m"
                        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                        resp = await client.get(url, headers=headers)
                        if resp.status_code == 200:
                            data = resp.json()
                            results = data.get("chart", {}).get("result", [])
                            if results:
                                meta = results[0].get("meta", {})
                                price = meta.get("regularMarketPrice", 0)
                                if price:
                                        # Добавляем рандомного шума, чтоб график дергался как сумасшедший (юзеры любят экшен)
                                    price = price + (random.random() - 0.5) * 0.05
                                    BINANCE_CACHE[sym.upper()] = price
                                    ticks.append({
                                        "symbol": sym.upper(),
                                        "price": price,
                                        "volume": meta.get("regularMarketVolume", 0)
                                    })
                    except Exception as e:
                        # Типичный Яху — отваливается когда ему вздумается
                        print(f"Failed to fetch {sym} from Yahoo:", e)
                
                if ticks:
                    await websocket.send_text(json.dumps({
                        "type": "MARKET_TICK",
                        "data": ticks
                    }))
                await asyncio.sleep(5)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"[Yahoo WS Error]: {e} (Походу опять Rate Limit поймали 🤡)")
        await websocket.close(code=1011, reason="Upstream Disconnected")

async def binance_realtime_proxy(websocket: WebSocket, symbols: list[str]):
    # Подсос к вебсокетам Бинанса (молимся чтобы Цзяо не отрубил нам доступ)
    binance_streams = [f"{sym.lower()}usdt@trade" for sym in symbols]
    stream_url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(binance_streams)}"
    try:
        async with websockets.connect(stream_url) as binance_ws:
            print(f"[Binance WS] Connected to streams: {binance_streams}")
            while True:
                response = await binance_ws.recv()
                data = json.loads(response)
                if "data" in data and "p" in data["data"]:
                    trade = data["data"]
                    stock_symbol = trade["s"].replace("USDT", "")
                    price = float(trade["p"])
                    volume = float(trade["q"])
                    BINANCE_CACHE[stock_symbol] = price
                    tick = {
                        "symbol": stock_symbol,
                        "price": price,
                        "volume": volume
                    }
                    await websocket.send_text(json.dumps({
                        "type": "MARKET_TICK",
                        "data": [tick]
                    }))
    except Exception as e:
        print(f"[Binance WebSocket Error]: {e}")
        await websocket.close(code=1011, reason="Upstream Disconnected")

@router.websocket("/ws/market")
async def websocket_market(websocket: WebSocket, symbols: str = Query("")):
    await websocket.accept()
    sym_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    
    if not sym_list:
        # Чел пришел без тикеров. Нафига вообще подключался?
        await websocket.close(code=1008, reason="No symbols provided")
        return

    crypto_syms = []
    stock_syms = []
    for sym in sym_list:
        if sym in ["AAPL", "TSLA", "MSFT", "GOOGL", "NVDA", "AMZN", "META"]:
            stock_syms.append(sym)
        else:
            crypto_syms.append(sym)

    tasks = []
    try:
        if crypto_syms:
            tasks.append(asyncio.create_task(binance_realtime_proxy(websocket, crypto_syms)))
        if stock_syms:
            tasks.append(asyncio.create_task(yahoo_finance_proxy(websocket, stock_syms)))
        
        while True:
            data = await websocket.receive_text()
            
    except WebSocketDisconnect:
        print(f"Client disconnected from symbols: {symbols}")
    finally:
        for t in tasks:
            t.cancel()
