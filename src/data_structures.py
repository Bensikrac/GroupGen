class Participant:
    """data structure, which represents a participant by storing name and attribute list of an individual participant"""

    __name: str
    attributes: dict[str, str]
    """attributes are mapped using attribute name ex. 'course' -> 'math' """

    def __init__(self, name: str):
        """Creates a participant with the name set. For groups Names should be unique"""
        self.__name = name

    def __init__(self, name: str, attributes: dict[str, str]):
        """Creates a new participant with the given name and attributes. Attributes are given in a dict of str->List[str]"""
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
        return self.__name == other.__name


class Group:
    """data structure which represents a group of participants"""

    __members: list[Participant]

    def __init__(self):
        """creates an empty group"""

    def __init__(self, members: list[Participant]):
        """creates a group with the given participants"""
        self.__members = members

    def get_members(self) -> list[Participant]:
        """returns all participants of the given group"""
        return self.__members

    def add_participant(self, participant: Participant):
        """adds the given participant to the group"""
        self.__members.append(participant)

    def remove_participant(self, participant: Participant):
        """removes the given participant from the group"""
        self.__members.remove(participant)
