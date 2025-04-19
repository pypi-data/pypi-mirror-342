"""Expert Application"""

import os

from binance.spot import Spot
from flask import Flask, render_template, jsonify

from logger import get_logger

logger = get_logger(__name__)
app = Flask(__name__)


@app.route("/")
def index():
    spot = Spot()
    infos = spot.exchange_info()
    symbols = infos["symbols"]

    context = {
        "title": "Home",
        "url": "/",
        "infos": infos,
        "symbols": symbols
    }
    return render_template("views/templates/views/home.tmpl", **context)


@app.route("/about")
def about():
    # import pandas
    # from lightweight_charts import Chart
    # chart = Chart()
    # df = pandas.read_csv("data/ohlcv.csv")
    # chart.set(df)
    # print(chart)

    context = {
        "title": "About",
        "url": "/about"
    }
    return render_template("views/templates/views/about.tmpl", **context)


@app.route("/account")
def account():
    """{
          "accountType": "SPOT",
          "balances": [
            {
              "asset": "ETH",
              "free": "1.00000000",
              "locked": "0.00000000"
            },
            {
              "asset": "BTC",
              "free": "1.00000000",
              "locked": "0.00000000"
            },
            {
              "asset": "LTC",
              "free": "8.00000000",
              "locked": "0.00000000"
            },
            ...
            {
              "asset": "BANANA",
              "free": "14.00000000",
              "locked": "0.00000000"
            },
            {
              "asset": "RENDER",
              "free": "104.00000000",
              "locked": "0.00000000"
            }
          ],
          "brokered": false,
          "buyerCommission": 0,
          "canDeposit": true,
          "canTrade": true,
          "canWithdraw": true,
          "commissionRates": {
            "buyer": "0.00000000",
            "maker": "0.00000000",
            "seller": "0.00000000",
            "taker": "0.00000000"
          },
          "makerCommission": 0,
          "permissions": [
            "SPOT"
          ],
          "preventSor": false,
          "requireSelfTradePrevention": false,
          "sellerCommission": 0,
          "takerCommission": 0,
          "uid": 1722358673636398520,
          "updateTime": 1723039532543
    }
    """
    from dotenv_vault import load_dotenv

    _ = load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = os.getenv("BINANCE_BASE_URL")

    spot = Spot(api_key, api_secret, base_url=base_url)
    __account = spot.account()
    return jsonify(__account)
    # return jsonify(__account["rateLimits"])


@app.route("/exchange")
def exchange():
    """{
    timezone: "UTC",
    serverTime: 1633012903441,
    rateLimits: [
            {
              "interval": "MINUTE",
              "intervalNum": 1,
              "limit": 6000,
              "rateLimitType": "REQUEST_WEIGHT"
            },
            ...
        ]
    exchangeFilters: [],
    symbols: [
            {
              "allowTrailingStop": true,
              "allowedSelfTradePreventionModes": [
                "EXPIRE_TAKER",
                "EXPIRE_MAKER",
                "EXPIRE_BOTH"
              ],
              "baseAsset": "ETH",
              "baseAssetPrecision": 8,
              "baseCommissionPrecision": 8,
              "cancelReplaceAllowed": true,
              "defaultSelfTradePreventionMode": "EXPIRE_MAKER",
              "permissions": [],
              "quoteAsset": "BTC",
              "quoteAssetPrecision": 8,
              "quoteCommissionPrecision": 8,
              "quoteOrderQtyMarketAllowed": true,
              "quotePrecision": 8,
              "status": "TRADING", // "BREAK", "PRE_TRADING", "POST_TRADING", "END_OF_DAY", "HALT"
              "symbol": "ETHBTC",
              "filters": [
                {
                  "filterType": "PRICE_FILTER",
                  "maxPrice": "922327.00000000",
                  "minPrice": "0.00001000",
                  "tickSize": "0.00001000"
                },
                {
                  "filterType": "LOT_SIZE",
                  "maxQty": "100000.00000000",
                  "minQty": "0.00010000",
                  "stepSize": "0.00010000"
                },
                {
                  "filterType": "ICEBERG_PARTS",
                  "limit": 10
                },
                {
                  "filterType": "MARKET_LOT_SIZE",
                  "maxQty": "2077.27362125",
                  "minQty": "0.00000000",
                  "stepSize": "0.00000000"
                },
                {
                  "filterType": "TRAILING_DELTA",
                  "maxTrailingAboveDelta": 2000,
                  "maxTrailingBelowDelta": 2000,
                  "minTrailingAboveDelta": 10,
                  "minTrailingBelowDelta": 10
                },
                {
                  "askMultiplierDown": "0.2",
                  "askMultiplierUp": "5",
                  "avgPriceMins": 5,
                  "bidMultiplierDown": "0.2",
                  "bidMultiplierUp": "5",
                  "filterType": "PERCENT_PRICE_BY_SIDE"
                },
                {
                  "applyMaxToMarket": false,
                  "applyMinToMarket": true,
                  "avgPriceMins": 5,
                  "filterType": "NOTIONAL",
                  "maxNotional": "9000000.00000000",
                  "minNotional": "0.00010000"
                },
                {
                  "filterType": "MAX_NUM_ORDERS",
                  "maxNumOrders": 200
                },
                {
                  "filterType": "MAX_NUM_ALGO_ORDERS",
                  "maxNumAlgoOrders": 5
                }
              ],
              "icebergAllowed": true,
              "isMarginTradingAllowed": true,
              "isSpotTradingAllowed": true,
              "ocoAllowed": true,
              "orderTypes": [
                "LIMIT",
                "LIMIT_MAKER",
                "MARKET",
                "STOP_LOSS",
                "STOP_LOSS_LIMIT",
                "TAKE_PROFIT",
                "TAKE_PROFIT_LIMIT"
              ],
              "otoAllowed": true,
              "permissionSets": [
                [
                  "SPOT",
                  "MARGIN",
                  "TRD_GRP_004",
                  "TRD_GRP_005",
                  "TRD_GRP_006",
                  ...
                  "TRD_GRP_054"
                ]
              ]
            },
            ...
        ]
    }
    """
    __exchange = Spot().exchange_info()
    # return jsonify(__exchange)
    return jsonify(__exchange["symbols"])


@app.route("/hello")
def hello():
    return "Hello World!"


@app.errorhandler(404)
def not_found(error):
    title = "404"
    return render_template("views/templates/views/error.tmpl", title=title, error=error), 404


if __name__ == "__main__":
    logger.info("start app")

    app.run(port=5001, debug=True)

    logger.info("finish app")
