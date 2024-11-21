from abc import ABCMeta, abstractmethod
from typing import Self
from data_interface import DataInterface


class DataFilter[G, FG, P, FP](DataInterface[FG, FP], metaclass=ABCMeta):
    """Abstract Base Class for simple data filtering operations"""

    __wrapee: DataInterface[G, P]

    def __init__(self: Self, wrapee: DataInterface[G, P]) -> None:
        """Initializer. Require a `DataInterface` to wrap around"""
        self.__wrapee = wrapee

    @staticmethod
    @abstractmethod
    def get_filter(data: G) -> FG:
        """Filter `get` data from underlying `DataInterface`"""
        return None

    def get(self: Self) -> FG:
        """Use `get` filter on output of underlying `DataInterface` `get`"""
        return self.get_filter(self.__wrapee.get())

    @staticmethod
    @abstractmethod
    def put_filter(data: FP) -> P:
        """Filter `put` data from underlying `DataInterface`"""
        return None

    def put(self: Self, data: FP) -> None:
        """Use `put` filter on output of underlying `DataInterface` `put`"""
        return self.__wrapee.put(self.put_filter(data))
