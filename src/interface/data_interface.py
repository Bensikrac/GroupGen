from abc import ABC


class DataInterface(ABC):
    """Abstract Base Class for simple I/O operations"""

    @abstractmethod
    def get(self) -> Any:
        """get a set of data"""
        return None

    @abstractmethod
    def put(self, x: Any) -> None:
        """put a set of data"""
        return None
