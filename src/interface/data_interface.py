from abc import ABCMeta, abstractmethod


class IDataInput[T](metaclass=ABCMeta):
    """Abstract Base Class for uniformly getting data."""

    @abstractmethod
    def get(self) -> T:
        """Get arbitrary data of type :class:`T`

        :return: Data of type :class:`T`

        :meta public:
        """
        pass


class IDataInputTransformer[To, From](IDataInput[To], metaclass=ABCMeta):
    """Abstract Base Class for transforming input data using an uniform interface.

    Implements :class:`IDataInput[To]`.
    """

    __data_input: IDataInput[From]

    def __init__(self, data_input: IDataInput[From]) -> None:
        """Initialize :class:`IDataInputTransformer[To, From]`.

        :param data_input: The :class:`IDataInput[From]` the transformer will wrap around

        :meta public:
        """
        self.__data_input = data_input

    @staticmethod
    @abstractmethod
    def transform_get(x: From) -> To:
        """Transform input data of type :class:`From` to data of type :class:`To`.

        :param x: Data to transform, coming from wrapped :func:`IDataInput[From].get`

        :return: Transformed data.

        :meta public:
        """
        pass

    def get(self) -> To:
        """Get transformed data of type :class:`To`

        :return: Data of type :class:`From`, transformed to :class:`To` using :func:`transform_get`

        :meta public:
        """
        return self.transform_get(self.__data_input.get())


class IDataOutput[T](metaclass=ABCMeta):
    """Abstract Base Class for uniformly putting data."""

    @abstractmethod
    def put(self, x: T) -> None:
        """Put arbitrary data of type :class:`T`

        :return: Data of type :class:`T`

        :meta public:
        """
        pass


class IDataOutputTransformer[From, To](IDataOutput[From], metaclass=ABCMeta):
    """Abstract Base Class for transforming output data using an uniform interface.

    Implements :class:`IDataInput[From]`.
    """

    __data_output: IDataOutput[To]

    def __init__(self, data_output: IDataOutput[To]) -> None:
        """Initialize :class:`IDataOutputTransformer[From, To]`.

        :param data_output: The :class:`IDataOutput[To]` the transformer will wrap around

        :meta public:
        """
        self.__data_output = data_output

    @staticmethod
    @abstractmethod
    def transform_put(x: From) -> To:
        """Transform output data of type :class:`From` to data of type :class:`To`.

        :param x: Data to transform

        :return: Transformed data, forwarded to wrapped :func:`IDataOutput[To].put`

        :meta public:
        """
        pass

    def put(self, x: From) -> None:
        """Put data of type :class:`From` transformed to type :class:`To`

        :param x: Data of type :class:`From` to transform and put

        :meta public:
        """
        return self.__data_output.put(self.transform_put(x))
