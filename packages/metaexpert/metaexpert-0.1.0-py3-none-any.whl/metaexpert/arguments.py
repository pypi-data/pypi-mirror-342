"""Arguments for the trading bot."""

import argparse

from metaexpert.config import (
    CONTRACT_TYPE_COIN_M,
    CONTRACT_TYPE_USD_M,
    DEFAULT_CONTRACT_TYPE,
    DEFAULT_MODE,
    DEFAULT_TIMEFRAME,
    DEFAULT_TRADE_TYPE,
    LOG_LEVEL,
    MAX_POSITION_SIZE,
    MODE_BACKTEST,
    MODE_LIVE,
    MODE_PAPER,
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT,
    TRADE_TYPE_FUTURES,
    TRADE_TYPE_MARGIN,
    TRADE_TYPE_OPTIONS,
    TRADE_TYPE_SPOT,
    TRAILING_STOP_PERCENT,
    TRADING_PAIRS,
)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Expert Trading Bot")

    parser.add_argument(
        "--type",
        type=str,
        choices=[TRADE_TYPE_SPOT, TRADE_TYPE_FUTURES, TRADE_TYPE_OPTIONS, TRADE_TYPE_MARGIN],
        default=DEFAULT_TRADE_TYPE,
        help="Trading type: spot, futures, options, or margin",
    )
    parser.add_argument(
        "--contract",
        type=str,
        choices=[CONTRACT_TYPE_USD_M, CONTRACT_TYPE_COIN_M],
        default=DEFAULT_CONTRACT_TYPE,
        help="Contract type for futures trading: USDⓈ-M (usd_m) or COIN-M (coin_m)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=[MODE_BACKTEST, MODE_PAPER, MODE_LIVE],
        default=DEFAULT_MODE,
        help="Trading mode: backtest, paper, or live",
    )
    parser.add_argument(
        "--pair",
        type=str,
        default=TRADING_PAIRS[0],
        help="Trading pair (e.g., BTCUSDT)",
    )
    parser.add_argument(
        "--timeframe",
        "--tf",
        type=str,
        default=DEFAULT_TIMEFRAME,
        help="Trading timeframe",
    )
    parser.add_argument(
        "--size",
        "--lots",
        type=float,
        default=MAX_POSITION_SIZE,
        help="Maximum position size as a fraction of available balance",
    )
    parser.add_argument(
        "--stop-loss",
        "--sl",
        type=float,
        default=STOP_LOSS_PERCENT,
        help="Stop loss percentage",
    )
    parser.add_argument(
        "--take-profit",
        "--tp",
        type=float,
        default=TAKE_PROFIT_PERCENT,
        help="Take profit percentage",
    )
    parser.add_argument(
        "--trailing-stop",
        "--ts",
        type=float,
        default=TRAILING_STOP_PERCENT,
        help="Trailing stop percentage",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=LOG_LEVEL,
        help="Logging level",
    )
    return parser.parse_args()
