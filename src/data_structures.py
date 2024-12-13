"""Data structures module"""

from typing import TypeVar
from dataclasses import dataclass


@dataclass(
    init=True,
    repr=True,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=True,
    match_args=True,
    kw_only=False,
    slots=False,
    weakref_slot=False,
)
class Participant:
    """Structure representing a participant

    :param uid: unique id for participant
    :param attributes: list of attributes for participants
    """

    __uid: int
    __attributes: dict[str, str]
    # attributes maps from attribute class to attribute value

    def __init__(self, uid: str, attributes: dict[str, str]) -> None:
        self.__uid = uid
        self.__attributes = attributes

    @property
    def uid(self) -> int:
        """UID of the :class:`Participant`.

        :return: UID of the :class:`Participant`
        """
        return self.__uid

    @property
    def attributes(self) -> dict[str, str]:
        """Attributes of the :class:`Participant`.

        :return: Attributes of the :class:`Participant`
        """
        return self.__attributes

    def __getitem__(self, attribute: str) -> str:
        return self.attributes[attribute]

    def get_attribute(self, attribute: str) -> str:
        """Return the attribute value of the given attribute for the :class:`Participant`.

        :param attribute: Attribute of which the value is returned

        :return: Attribute value of the given attribut for the :class:`Participant`
        """
        return self.attributes[attribute]

    def __eq__(self, other: "Participant") -> bool:
        return self.__uid == other.uid

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
