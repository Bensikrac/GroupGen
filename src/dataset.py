"""Dataset module."""

from excel_tool import read_excel
from data_structures import Participant


class Dataset:
    """Class representing a set of (input) data.

    :param location: The location of the raw data. Currently supported: paths to Excel files
    """

    __raw_data: list[list[str]]
    __normalized_data: list[list[str]]
    __participants: set[Participant]
    __number_of_participants: int
    __attribute_classes: list[str]
    __number_of_attribute_classes: int

    @staticmethod
    def __parse_participant(
        uid: int, attribute_classes: iterable[str], attribute_values: iterable[str]
    ) -> Participant:
        """Convert a UID, a list of attribute classes and
        a list of attribute values to a :class:`Participant`.

        :param uid: UID for the new :class:`Participant`
        :param attribute_classes: List of attribute classes for the new :class:`Participant`
        :param attribute_values: List of attribute values for the new :class:`Participant`

        :return: A new :class:`Participant`
        """
        if len(attribute_classes) != len(attribute_values):
            raise ValueError(
                "attribute_classes and attribute_values are not the same size"
            )
        return Participant(uid, dict(zip(attribute_classes, attribute_values)))

    def __init__(self, location: str) -> None:
        # check location type
        if location.endswith(".xlsx") or location.endswith(".xls"):
            # Excel
            self.__raw_data = read_excel(location)
            # pylint: disable=W0511
            # TODO: add normalization
            self.__normalized_data = self.__raw_data
        else:
            # ...
            raise NotImplementedError

        self.__participants = {}

        for i, row in enumerate(self.__normalized_data):
            if i == 0:
                # first row is the attribute classes
                self.__attribute_classes = row
                self.__number_of_attribute_classes = len(self.__attribute_classes)
            else:
                # other rows are the :class:`Participant`s
                self.__participants &= {
                    self.__parse_participant(i, self.__attribute_classes, row)
                }
        self.__number_of_participants = len(self.__participants)

    @property
    def raw(self) -> list[list[str]]:
        """Raw base data"""
        return self.__raw_data

    @property
    def normalized(self) -> list[list[str]]:
        """Normalized base data"""
        return self.__normalized_data

    @property
    def participants(self) -> set[Participant]:
        """Set of all :class:`Participant`s."""
        return self.__participants

    @property
    def number_of_participants(self) -> int:
        """Number of all :class:`Participant`s."""
        return self.__number_of_participants

    @property
    def attribute_classes(self) -> list[str]:
        """List of all attribute classes."""
        return self.__attribute_classes

    @property
    def number_of_attribute_classes(self) -> int:
        """Number of all attribute classes."""
        return self.__number_of_attribute_classes
