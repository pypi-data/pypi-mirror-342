"""Trade
"""
from dataclasses import dataclass
from typing import Any

from logger import get_logger

_logger = get_logger(__name__)


@dataclass
class Trade:
    """Trade
    """

    def __init__(self, symbol: str | None, **props: dict[str, Any]) -> None:
        self.symbol = symbol
        self._lots = props.get("lots", 0)
        self._stop_loss = props.get("stop_loss", 0)
        self._take_profit = props.get("take_profit", 0)
        self._trailing_stop = props.get("trailing_stop", 0)
        self._positions = props.get("positions", 0)
        self._slippage = props.get("slippage", 0)

    def trade(
            self,
            *,
            lots: float = 0,
            stop_loss: float = 0,
            take_profit: float = 0,
            trailing_stop: float = 0,
            positions: int = 0,
            slippage: int = 0
    ) -> None:
        self._lots = lots
        self._stop_loss = stop_loss
        self._take_profit = take_profit
        self._trailing_stop = trailing_stop
        self._positions = positions
        self._slippage = slippage

    # POSITION
    def open_position(self, side: str) -> bool:
        return False

    def close_position(self, side: str) -> bool:
        return False

    def close_all_positions(self, side: str) -> bool:
        return False

    def modify_position(self) -> bool:
        return False

    def modify_all_positions(self) -> bool:
        return False

    # ORDER
    def open_order(self, side: str) -> bool:
        return False

    def close_order(self, side: str) -> bool:
        return False

    def close_all_orders(self, side: str) -> bool:
        return False

    # @property
    # def lots(self) -> float:
    #     return self._lots
    #
    # @lots.setter
    # def lots(self, value: float) -> None:
    #     self._lots = value
    #
    # @property
    # def stop_loss(self) -> float:
    #     return self._stop_loss
    #
    # @stop_loss.setter
    # def stop_loss(self, value: float) -> None:
    #     self._stop_loss = value
    #
    # @property
    # def take_profit(self) -> float:
    #     return self._take_profit
    #
    # @take_profit.setter
    # def take_profit(self, value: float) -> None:
    #     self._take_profit = value
    #
    # @property
    # def trailing_stop(self) -> float:
    #     return self._trailing_stop
    #
    # @trailing_stop.setter
    # def trailing_stop(self, value: float) -> None:
    #     self._trailing_stop = value
    #
    # @property
    # def positions(self) -> int:
    #     return self._positions
    #
    # @positions.setter
    # def positions(self, value: int) -> None:
    #     self._positions = value
    #
    # @property
    # def slippage(self) -> int:
    #     return self._slippage
    #
    # @slippage.setter
    # def slippage(self, value: int) -> None:
    #     self._slippage = value

#    datetime          m_long_timer;
#    datetime          m_short_timer;
#    int               m_long_position;
#    int               m_short_position;
#
#    bool              CheckParameters(void);
#    bool              CheckLots(void);
#    void              CheckingAbilityOpenTransactions(void);
#    double            MarginCheck(const ENUM_ORDER_TYPE type, const double price) const;
#    double            FreeMarginCheck(const ENUM_ORDER_TYPE type, const double price) const;
