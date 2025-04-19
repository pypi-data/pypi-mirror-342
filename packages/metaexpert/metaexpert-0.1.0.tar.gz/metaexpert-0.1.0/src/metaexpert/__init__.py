""" """

from logger import get_logger, Logger
from metaexpert._process import Process


class MetaExpert(Process):
    """Expert trading system"""

    name: str

    def __init__(self):
        self.logger: Logger = get_logger(__name__)
        super().__init__(self.name)

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r}>"

    def run(self):
        pass

    from metaexpert._market import Market
    from metaexpert._trade import Trade
