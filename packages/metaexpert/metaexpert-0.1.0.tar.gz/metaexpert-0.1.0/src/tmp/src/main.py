"""Main module."""

import csv
import datetime

from binance.spot import Spot

from metaexpert.config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL

if __name__ == "__main__":

    print(BINANCE_API_KEY)
    print(BINANCE_API_SECRET)
    print(BINANCE_BASE_URL)

    client = Spot()

    # Get server timestamp
    print(client.time())

    # Get klines of BTCUSDT at 1m interval
    candles = client.klines(symbol="BTCUSDT", interval="1m", limit=5)
    with open("data/candles_BTCUSDT_1m.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for candle in candles:
            writer.writerow(candle)
            # print(*candle)

    candles = client.klines(
        symbol="BNBUSDT",
        interval="1h",
        startTime=int(datetime.datetime(2024, 7, 29).timestamp() * 1000),
        endTime=int(datetime.datetime(2024, 8, 4).timestamp() * 1000),
    )
    with open("data/candles_BNBUSDT_1h_history.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for candle in candles:
            writer.writerow(candle)

    # api key/secret are required for user data endpoints
    client = Spot(
        BINANCE_API_KEY,
        BINANCE_API_SECRET,
        base_url=BINANCE_BASE_URL,
    )

    # Get account and balance information
    print(client.account())
    print(client.ping())

    # Post a new order
    # params = {
    #     "symbol": "BTCUSDT",
    #     "side": "SELL",
    #     "type": "LIMIT",
    #     "timeInForce": "GTC",
    #     "quantity": 0.002,
    #     "price": 61000,
    # }
    #
    # response = client.new_order(**params)
    # print(response)
    #
    # order = client.get_order(symbol="BTCUSDT", orderId=response["orderId"])
    # print(order)
    #
    # response = client.cancel_open_orders(symbol="BTCUSDT")
    # print(response)

    # ta.MA()
