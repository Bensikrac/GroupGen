from abc import ABCMeta, abstractmethod


class DataInterface[G, P](metaclass=ABCMeta):
    """Abstract Base Class for simple I/O operations

    Generic arguments:
    G -- return type of `get`
    P -- argument type of `put`
    """

    @abstractmethod
    def get(self) -> G:
        """get an arbitrary set of data"""
        pass

    @abstractmethod
    def put(self, x: P) -> None:
        """put an arbitrary set of data"""
        pass
