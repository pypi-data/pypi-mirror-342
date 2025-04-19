"""
Payload:

{
  "e": "kline",     // Event type
  "E": 1672515782136,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 123400000, // Kline start time
    "T": 123460000, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}
"""

import asyncio
import json

import websockets

streams = [
    "btcusdt@kline_1m",
    "btcusdt@kline_5m",
    "ethusdt@kline_1m",
    "ethusdt@kline_5m",
    "xprusdt@kline_1m",
    "xprusdt@kline_5m",
]


async def subscribe_to_streams():
    url = "wss://stream.binance.com:9443/stream?streams="

    async with websockets.connect(url) as websocket:
        subscribe_request = {"method": "SUBSCRIBE", "params": streams, "id": 1}

        await websocket.send(json.dumps(subscribe_request))

        response = json.loads(await websocket.recv())
        print(response)

        async for message in websocket:
            data = json.loads(message)
            symbol = data.get("data", {}).get("k", {}).get("s")
            price = data.get("data", {}).get("k", {}).get("o")

            print(f"Received data for stream: {data}")
            print(f"Raw payload: {symbol}")
            print(f"Open price: {price}")


if __name__ == "__main__":
    asyncio.run(subscribe_to_streams())
