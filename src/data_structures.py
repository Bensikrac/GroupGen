"""Data structures module"""

from typing import TypeVar


class Participant:
    """Structure representing a participant

    :param uid: unique id for participant
    :param attributes: list of attributes for participants
    """

    __uid: int
    attributes: dict[str, str]
    # attributes from attribute to it's value

    def __init__(self, uid: str, attributes: dict[str, str]) -> None:
        self.__uid = uid
        self.attributes = attributes

    @property
    def uid(self) -> int:
        """UID of the :class:`Participant`.

        :return: UID of the :class:`Participant`
        """
        return self.__uid

    def get_attribute(self, attribute: str) -> str:
        """Return the attribute value of the given attribute for the :class:`Participant`.

        :param attribute: Attribute of which the value is returned

        :return: Attribute value of the given attribut for the :class:`Participant`
        """
        return self.attributes[attribute]

    def set_attribute(self, attribute: str, value: str) -> None:
        """Set the given attribute to the given value for the :class:`Participant`.

        :param attribute: Attribute to be set (already existing)
        :param value: Value for the attribute
        """
        self.attributes[attribute] = value

    def __eq__(self, other: "Participant") -> bool:
        return self.__uid == other.uid

    def __repr__(self) -> str:
        return f"Participant({self.__uid}, {self.attributes})"

    def __str__(self) -> str:
        return f"UID: {self.__uid} Attributes: {self.attributes}"

    def __hash__(self) -> int:
        return self.__uid


type Group = set[Participant]
type Iteration = list[Group]
type Assignment = list[Iteration]


# pylint: disable=invalid-name
#: Generic type variable
type T = TypeVar("T")

type ListOfRowLists[T] = list[list[T]]
type ListOfColumnLists[T] = list[list[T]]
