from abc import ABCMeta, abstractmethod
from data_interface import DataInterface


class DataMap[G, MG, P, MP](DataInterface[MG, MP], metaclass=ABCMeta):
    """Abstract Base Class for simple data mapping operations
    Implements `DataInterface[MG, MP]`

    Has a `DataInterface` (wrapee) of which it maps the I/O.

    Generic arguments:
    G -- return type of wrapee `get`
    MG -- return type of mapping `map_get`
    P -- argument type of wrapee `put`
    MP -- argument type of mapping `map_put`
    """

    __wrapee: DataInterface[G, P]

    def __init__(self, wrapee: DataInterface[G, P]) -> None:
        """Initializer. Require a `DataInterface` to wrap around

        Arguments:
        self -- current object
        wrapee -- `DataInterface` to wrap around
        """
        self.__wrapee = wrapee

    @staticmethod
    @abstractmethod
    def map_get(x: G) -> MG:
        """Static function, mapping the output from `get` of wrapee"""
        pass

    def get(self) -> MG:
        """Map `get` of wrapee using `map_get`"""
        return self.map_get(self.__wrapee.get())

    @staticmethod
    @abstractmethod
    def map_put(x: MP) -> P:
        """Static function, mapping the input for `put` of wrapee"""
        pass

    def put(self, x: MP) -> None:
        """Map input for `put` of wrapee using `map_put`"""
        return self.__wrapee.put(self.map_put(x))
