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

    def __init__(self, uid: int, attributes: dict[str, str] = None):
        if attributes is None:
            attributes = {}
        self.__uid = uid
        self.attributes = attributes

    def get_uid(self) -> int:
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
        return isinstance(other, Participant) and self.get_uid() == other.get_uid()

    def __repr__(self) -> str:
        return "Participant(" + self.__uid + ", " + str(self.attributes) + ")"

    def __str__(self) -> str:
        return "Name: " + self.__uid + " Attribute: " + str(self.attributes)

    def __hash__(self) -> int:
        return hash(self.__uid)


type Group = set[Participant]
type Iteration = list[Group]
type Assignment = list[Iteration]
