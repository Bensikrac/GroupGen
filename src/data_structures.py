"""Data structures module"""


class Participant:
    """Structure representing a participant

    :param uid: unique id for participant
    :param attributes: list of attributes for participants
    """

    __uid: int
    attributes: dict[str, str]
    # attributes from attribute to it's value

    def __init__(self, uid: str, attributes: dict[str, str] | None = None) -> None:
        if attributes is None:
            attributes = {}
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
        return f"Name: {self.__uid} Attributes: {self.attributes}"

    def __hash__(self) -> int:
        return self.__uid


type Group = set[Participant]
type Iteration = list[Group]
type Assignment = list[Iteration]


def combine_outer(x: list[list[str]], y: list[list[str]]) -> list[list[str]]:
    """Combine 2 2-dimensional lists by the outer lists.

    Outer-list-wise appending :param:`y` to :param:`x`

    :param x: List
    :param y: List

    :return: Combined list
    """
    return x + y


def combine_inner(x: list[list[str]], y: list[list[str]]) -> list[list[str]]:
    """Combine 2 2-dimensional lists by their inner lists.

    Inner-list-wise appending :param:`y` to :param:`x`

    :param x: List
    :param y: List

    :return: Combined list
    """
    # make x and y same sized
    if len(x) < len(y):
        x += [[str()]] * (len(y) - len(x))
    elif len(y) < len(x):
        y += [[str()]] * (len(x) - len(y))

    retval: list[list[str]] = []
    for a, b in zip(x, y):
        retval.append(a + b)
    return retval


def empty_row(n: int) -> list[list[str]]:
    """Create a string matrix with an empty row of size :param:`n`.

    :param n: Size of the row

    :return: String matrix with one row of size :param:`n`
    """
    return [[str()] * n]


def empty_column(n: int) -> list[list[str]]:
    """Create a string matrix with an empty column of size :param:`n`.

    :param n: Size of the column

    :return: String matrix with :param:`n` rows of size 1
    """
    return list([[str()]] * n)


def participant_to_str_matrix(participant: Participant) -> list[list[str]]:
    """Convert a :class:`Participant` to a string matrix.

    :param participant: :class:`Participant` to convert

    :return: String matrix of converted :class:`Participant`
    """
    return [[str(participant)]]


def group_to_str_matrix(group: Group) -> list[list[str]]:
    """Convert a :class:`Group` to a string matrix.

    :param group: :class:`Group` to convert

    :return: String matrix of converted :class:`Group`
    """
    retval: list[list[str]] = []
    for participant in group:
        retval = combine_outer(retval, participant_to_str_matrix(participant))
    return retval


def iteration_to_str_matrix(iteration: Iteration) -> list[list[str]]:
    """Convert a :class:`Iteration` to a string matrix.

    :param iteration: :class:`Iteration` to convert

    :return: String matrix of converted :class:`Iteration`
    """
    retval: list[list[str]] = []
    for i, group in enumerate(iteration):
        if i == 0:
            retval = group_to_str_matrix(group)
        else:
            retval = combine_inner(retval, empty_column(len(group)))
            retval = combine_inner(retval, group_to_str_matrix(group))
    return retval


def assignment_to_str_matrix(assignment: Assignment) -> list[list[str]]:
    """Convert a :class:`Assignment` to a string matrix.

    :param assignment: :class:`Assignment` to convert

    :return: String matrix of converted :class:`Assignment`
    """
    retval: list[list[str]] = [["Assignment"]]
    for i, iteration in enumerate(assignment):
        if i != 0:
            retval = combine_outer(retval, empty_row(len(retval[-1])))
        retval = combine_outer(retval, [[f"Iteration {i+1}"]])
        retval = combine_outer(retval, iteration_to_str_matrix(iteration))
    return retval
