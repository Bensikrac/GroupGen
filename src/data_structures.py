from typing import Dict, List

class Participant:
    __name: str
    __attributes: Dict[str, List[str]]
    """attributes are mapped using attribute name ex. 'interest' -> ['math', 'physics']"""
    
    def __init__(name: str):
        """Creates a participant with the name set. For groups Names should be unique"""
        self.__name = name
    
    def __init__(name: str, attributes: Dict[str, List[str]]):
        """Creates a new participant with the given name and attributes. Attributes are given in a dict of str->List[str]"""
        self.__name = name
        self.__attributes = attributes

    def get_name(self) -> str:
        return self.__name

    def get_attributes(self) -> Dict[str, List[str]]:
        return self.__attributes

    def get_attribute(self, attribute_name: str) -> List[str]:
        return self.__attributes[attribute_name]

    def set_attributes(self, attributes: Dict[str, List[str]]):
        """ overwrites all attributes of the participant with the given attribute list"""
        self.__attributes = attributes

    def set_attribute(self, attribute_name: str, attribute_values: List[str]):
        """ overwrites the given attribute name with the given attribute value"""
        self.__attributes[attribute_name] = attribute_values

    def add_attribute_value(self, attribute_name: str, attribute_value: str):
        """ adds a single value to the list of attribute values for the given attribute name"""
        self.__attributes[attribute_name].append(attribute_value)

    def remove_attribute_value(self, attribute_name: str, attribute_value: str):
        """ removes the given attribute value from the attribute name"""
        self.__attributes[attribute_name].remove(attribute_value)


    def __eq__(self, other) -> bool:
        """Compares if two participants are equal, based on their name"""
        return self.__name == other.__name


class Group:
    __members: List[Participant]

    def __init__():
        """ creates an empty group """

    def __init__(members: List[Participant]):
        """ creates a group with the given participants """
        self.__members = members
    
    def add_participant(self, participant: Participant):
        """ adds the given participant to the group """
        self.__members.append(participant)

    def remove_participant(self, participant: Participant):
        """ removes the given participant from the group """
        self.__members.remove(participant)
    
    def get_participants(self) -> List[Participant]:
        """ returns list of members """
        return self.__members