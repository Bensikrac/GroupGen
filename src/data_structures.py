"""Data structures module"""


class Participant:
    """data structure, which represents a participant by storing unique id and
    attribute list of an individual participant

    :param uid: unique id for participant
    :param attributes: list of attributes for participants
    """

    __uid: int
    attributes: dict[str, str]
    # attributes are mapped using attribute name ex. 'course' -> 'math'

    def __init__(self, uid: str, attributes: dict[str, str] = None):
        if attributes is None:
            attributes = {}
        self.__uid = uid
        self.attributes = attributes

    def get_uid(self) -> str:
        """Returns the uid of the participant.

        :return: unique id of the participant
        """
        return self.__uid

    def get_attribute(self, attribute: str) -> str:
        """Returns the attribute value of the given attribute for the participant.

        :param attribute: attribute of which the value is returned

        :return: attribute value of the given attribut for the participant
        """
        return self.attributes[attribute]

    def set_attribute(self, attribute: str, value: str) -> None:
        """Sets the given attribute to the given value for the participant.

        :param attribute: attribute to be set for participant (already existing)
        :param value: value given to the given attribute
        """
        self.attributes[attribute] = value

    def __eq__(self, other) -> bool:
        return self.__uid == other.__uid

    def __repr__(self) -> str:
        return f"Participant({self.__uid}, {self.attributes})"

    def __str__(self) -> str:
        return f"Name: {self.__uid} Attribute: {self.attributes}"

    def __hash__(self) -> int:
        return self.__uid


type Group = set[Participant]
type Iteration = list[Group]
type Assignment = list[Iteration]


def combine_outer[T](x: list[list[T]], y: list[list[T]]) -> list[list[T]]:
    return x + y


def combine_inner[T](x: list[list[T]], y: list[list[T]]) -> list[list[T]]:
    # if len(x) < 1 or len(y) < 1 or len(x[0]) != len(y[0]):
    #    raise ValueError("x and y not same size")
    if len(x) < len(y):
        x += [[str()]] * (len(y) - len(x))
    elif len(y) < len(x):
        y += [[]] * (len(x) - len(y))
    retval: list[list[str]] = []
    for a, b in zip(x, y):
        retval.append(a + b)
    return retval


def empty_row(n: int) -> list[list[str]]:
    return [[str()] * n]


def empty_column(n: int) -> list[list[str]]:
    return list([[str()]] * n)


def participant_to_str_matrix(participant: Participant) -> list[list[str]]:
    return [[str(participant)]]


def group_to_str_matrix(group: Group) -> list[list[str]]:
    retval: list[list[str]] = []
    for participant in group:
        retval = combine_outer(retval, participant_to_str_matrix(participant))
    return retval


def iteration_to_str_matrix(iteration: Iteration) -> list[list[str]]:
    retval: list[list[str]] = []
    for i, group in enumerate(iteration):
        if i == 0:
            retval = group_to_str_matrix(group)
        else:
            retval = combine_inner(retval, empty_column(len(group)))
            retval = combine_inner(retval, group_to_str_matrix(group))
    return retval


def assignment_to_str_matrix(assignment: Assignment) -> list[list[str]]:
    retval: list[list[str]] = [["Assignment"]]
    for i, iteration in enumerate(assignment):
        if i != 0:
            retval = combine_outer(retval, empty_row(len(retval[-1])))
        retval = combine_outer(retval, [[f"Iteration {i+1}"]])
        retval = combine_outer(retval, iteration_to_str_matrix(iteration))
    return retval
