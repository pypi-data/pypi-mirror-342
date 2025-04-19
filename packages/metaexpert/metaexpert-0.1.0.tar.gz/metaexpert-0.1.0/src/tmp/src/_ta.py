import talib
from numpy import genfromtxt

if __name__ == "__main__":
    data = genfromtxt("data/candles_BNBUSDT_1h_history.csv", delimiter=",")

    close = data[:, 4]
    # print(close)

    # close = numpy.random.randn(100)

    # sma = talib.MA(close, timeperiod=3, matype=talib.MA_Type.SMA)
    # print(sma)
    #
    # ema = talib.MA(close, timeperiod=3, matype=talib.MA_Type.EMA)
    # print(ema)
    #
    rsi = talib.RSI(close, timeperiod=5)
    print(rsi)
