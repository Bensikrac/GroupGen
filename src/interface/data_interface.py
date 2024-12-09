"""Data interface module."""

# pylint disable=too-few-public-methods,unnecessary-pass

from abc import abstractmethod
from typing import Protocol, TypeVar


#: Generic type variable
type T = TypeVar("T")


class IDataInput[T](Protocol):
    """Protocol for data input."""

    @abstractmethod
    def get(self) -> T:
        """Get arbitrary data of type :class:`T`.

        :return: Arbitrary data
        """
        pass


class IDataOutput[T](Protocol):
    """Protocol for data output."""

    @abstractmethod
    def put(self, x: T) -> None:
        """Put arbitrary data of :class:`T`.

        :param x: Arbitrary data to put
        """
        pass


#: Input type
type I = TypeVar("I")

#: Output type
type O = TypeVar("O")


class IDataIO[I, O](IDataInput[I], IDataOutput[O], Protocol):
    """Combined Protocol for data input/output."""

    pass


#: Type to convert from
type From = TypeVar("From")

#: Type to convert to
type To = TypeVar("To")


class IDataInputTransformer[From, To](Protocol):
    """Protocol for input transformers."""

    @staticmethod
    @abstractmethod
    def transform_get(x: From) -> To:
        """Transform arbitrary data of :class:`From` to :class:`To`.

        :param x: Arbitrary data

        :return: Transformed data
        """
        pass


class IDataOutputTransformer[From, To](Protocol):
    """Protocol for output transformers."""

    @staticmethod
    @abstractmethod
    def transform_put(x: From) -> To:
        """Transform arbitrary data of :class:`From` to :class:`To`.

        :param x: Arbitrary data

        :return: Transformed data
        """
        pass


class ITransformedDataInput[From, To](
    IDataInput[To], IDataInputTransformer[From, To], Protocol
):
    """Protocol for transformed data input.

    :param data_input: The underlying :class:`IDataInput` to which :func:`get` is forwarded
    """

    __data_input: type[IDataInput[From]]

    def __init__(self, data_input: type[IDataInput[From]]) -> None:
        self.__data_input = data_input

    def get(self) -> To:
        """Get arbitrary data of :class:`From`, transformed to :class:`To`.

        :return: Transformed data
        """
        return self.transform_get(self.__data_input.get())


class ITransformedDataOutput[From, To](
    IDataOutput[From], IDataOutputTransformer[From, To], Protocol
):
    """Protocol for transformed data output.

    :param data_output: The underlying :class:`IDataOutput` to which :func:`put` is forwarded
    """

    __data_output: type[IDataOutput[To]]

    def __init__(self, data_output: type[IDataOutput[To]]) -> None:
        self.__data_output = data_output

    def put(self, x: From) -> None:
        """Put arbitrary data of :class:`From`, transformed to :class:`To`.

        :param x: Data to transform and put
        """
        return self.__data_output.put(self.transform_put(x))


#: Type to convert input from
type IFrom = TypeVar("IFrom")

#: Type to convert input to
type ITo = TypeVar("ITo")

#: Type to convert output from
type OFrom = TypeVar("OFrom")

#: Type to convert output to
type OTo = TypeVar("OTo")


class ITransformedDataIO[IFrom, ITo, OFrom, OTo](
    IDataIO[ITo, OFrom],
    IDataInputTransformer[IFrom, ITo],
    IDataOutputTransformer[OFrom, OTo],
    Protocol,
):
    """Combined Protocol for transformed data input/output.

    :param data_io: The underlying :class:`IDataIO`
    """

    __data_io: type[IDataIO[IFrom, OTo]]

    def __init__(self, data_io: type[IDataIO[IFrom, OTo]]) -> None:
        self.__data_io = data_io

    def get(self) -> ITo:
        """Get arbitrary data of :class:`IFrom`, transformed to :class:`ITo`.

        :return: Transformed data
        """
        return self.transform_get(self.__data_io.get())

    def put(self, x: OFrom) -> None:
        """Put arbitrary data of :class:`OFrom`, transformed to :class:`OTo`.

        :param x: Data to transform and put
        """
        return self.__data_io.put(self.transform_put(x))


class ISymmetricDataIO[T](IDataIO[T, T], Protocol):
    """Convenience Protocol for symmetric data input/output."""

    pass


#: Process-facing type
type P = TypeVar("P")

#: Extern-facing type
type E = TypeVar("E")


class ISymmetricTransformedDataIO[P, E](ITransformedDataIO[E, P, P, E]):
    """Convenience Protocol for symmetric transformed data input/output."""

    pass
