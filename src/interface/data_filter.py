from abc import ABC
from data_interface import DataInterface


class DataFilter(ABC, DataInterface):
    """Abstract Base Class for simple data filtering operations"""

    __wrapee: DataInterface

    def __init__(self, wrapee: DataInterface):
        """Initializer. Require a `DataInterface` to wrap around"""
        self.__wrapee = wrapee

    @staticmethod
    @abstractmethod
    def get_filter(data: Any) -> Any:
        """Filter `get` data from underlying `DataInterface`"""
        return None

    def get(self) -> Any:
        """Use `get` filter on output of underlying `DataInterface` `get`"""
        return get_filter(self.__wrapee.get())

    @staticmethod
    @abstractmethod
    def put_filter(data: Any) -> Any:
        """Filter `put` data from underlying `DataInterface`"""
        return None

    def put(self, data: Any) -> None:
        """Use `put` filter on output of underlying `DataInterface` `put`"""
        return self.__wrapee.put(put_filter(data))
