class Participant:
    """data structure, which represents a participant by storing name and attribute list of an individual participant"""

    name: str
    attributes: dict[str, str]
    """attributes are mapped using attribute name ex. 'course' -> 'math' """
    
    def __init__(self, name: str):
        """Creates a participant with the name set. For groups Names should be unique"""
        self.name = name
    
    def __init__(self, name: str, attributes: dict[str, str]):
        """Creates a new participant with the given name and attributes. Attributes are given in a dict of str->List[str]"""
        self.name = name
        self.attributes = attributes

    def __eq__(self, other) -> bool:
        """Compares if two participants are equal, based on their name"""
        return self.name == other.name


class Group:
    """data structure which represents a group of participants"""

    members: list[Participant]

    def __init__(self):
        """creates an empty group"""

    def __init__(self, members: list[Participant]):
        """creates a group with the given participants"""
        self.members = members
    
    def add_participant(self, participant: Participant):
        """adds the given participant to the group"""
        self.members.append(participant)

    def remove_participant(self, participant: Participant):
        """removes the given participant from the group"""
        self.members.remove(participant)