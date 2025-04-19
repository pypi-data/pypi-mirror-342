import datetime

from binance.spot import Spot as Client
from flask import Flask, render_template, request, flash, redirect, jsonify

from metaexpert.config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL

app = Flask(__name__)


@app.route("/")
def index():
    title = "Chart View"
    account = client.account()
    balances = account["balances"]
    # symbols = account["symbols"]

    return render_template(
        "index.html", title=title, my_balances=balances  # , symbols=symbols
    )


@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/buy", methods=["POST"])
def buy():
    print(request.form)
    try:
        _order = client.new_order(
            symbol=request.form["symbol"],
            side="BUY",
            type="LIMIT",
            quantity=request.form["quantity"],
        )
    except Exception as e:
        flash(e.message, "error")

    return redirect("/")


@app.route("/sell")
def sell():
    return "sell"


@app.route("/settings")
def settings():
    return "settings"


@app.route("/history")
def history():
    candlesticks = client.klines(
        symbol="BNBUSDT",
        interval="1h",
        startTime=int(datetime.datetime(2024, 7, 29).timestamp() * 1000),
        endTime=int(datetime.datetime(2024, 8, 4).timestamp() * 1000),
    )

    processed_candlesticks = []
    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4],
        }
        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)


if __name__ == "__main__":
    client = Client(
        BINANCE_API_KEY,
        BINANCE_API_SECRET,
        base_url=BINANCE_BASE_URL,
    )

    app.run(debug=True)
