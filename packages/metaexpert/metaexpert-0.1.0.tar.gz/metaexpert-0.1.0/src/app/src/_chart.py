import pandas
from lightweight_charts import Chart  # , JupyterChart

from logger import get_logger

logger = get_logger()

if __name__ == "__main__":
    logger.info("start chart")
    chart = Chart()

    # Columns: time | open | high | low | close | volume
    df = pandas.read_csv("data/ohlcv.csv")
    chart.set(df)
    chart.show(block=True)

    # ju_chart = JupyterChart()
    # ju_chart.set(df)
    # ju_chart.load()
