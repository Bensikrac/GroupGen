"""Data structures module"""


class Participant:
    """data structure, which represents a participant by storing name and attribute list"""

    __name: str
    attributes: dict[str, str]
    """attributes are mapped using attribute name ex. 'course' -> 'math' """

    def __init__(self, name: str, attributes: dict[str, str] = None):
        """Creates a participant with the name set. For groups Names should be unique"""
        if attributes is None:
            attributes = {}
        self.__name = name
        self.attributes = attributes

    def get_name(self) -> str:
        """returns the name of the participant"""
        return self.__name

    def get_attribute(self, attribute: str) -> str:
        """returns the attribute value of the given attribute for the participant"""
        return self.attributes[attribute]

    def set_attribute(self, attribute: str, value: str):
        """sets the given attribute to the given value for the participant"""
        self.attributes[attribute] = value

    def __eq__(self, other) -> bool:
        """Compares if two participants are equal, based on their name"""
        return self.__name == other.get_name()

    def __repr__(self) -> str:
        return "Name: " + self.__name + " Attribute: " + str(self.attributes)



type Group = set[Participant]
type Round = list[Group]
type Assignment = list[Round]
