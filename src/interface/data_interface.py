from abc import ABCMeta, abstractmethod
from typing import Self


class DataInterface[G, P](metaclass=ABCMeta):
    """Abstract Base Class for simple I/O operations"""

    @abstractmethod
    def get(self: Self) -> G:
        """get a set of data"""
        return None

    @abstractmethod
    def put(self: Self, x: P) -> None:
        """put a set of data"""
        return None
