"""Data structures module"""

from typing import TypeVar
from dataclasses import dataclass


@dataclass(
    init=False,
    repr=True,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=False,
    match_args=True,
    kw_only=False,
    slots=False,
    weakref_slot=False,
)
class Participant:
    """Structure representing a participant.

    Initializer uses unnamed `int`s as UID and unnamed `dict`s as Attributes.
    Not passing a UID will cause it to assign a running number.
    Keyword arguments will be added to the Attributes.
    """

    current_uid: int = 0

    __uid: int
    __attributes: dict[str, str]
    # attributes maps from attribute class to attribute value

    def __init__(self, *args, **kwargs) -> None:
        self.__uid = None
        self.__attributes = None
        for arg in args:
            if isinstance(arg, int):
                self.__uid = arg
            if isinstance(arg, dict):
                self.__attributes = arg | kwargs

        if self.__uid is None:
            self.__uid = Participant.current_uid
            Participant.current_uid += 1

        if self.__attributes is None:
            self.__attributes = kwargs

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
        return self.__attributes[attribute]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Participant):
            return self.uid == other.uid
        return False

    def __str__(self) -> str:
        return f"UID: {self.__uid} Attributes: {self.attributes}"

    def __hash__(self) -> int:
        return self.uid


type Group = set[Participant]
type Iteration = list[Group]
type Assignment = list[Iteration]


# pylint: disable=invalid-name
#: Generic type variable
T = TypeVar("T")

type ListOfRowLists[T] = list[list[T]]
type ListOfColumnLists[T] = list[list[T]]
