from copy import copy
from typing import Any
from data_structures import AttributeUID, AttributeValueUID, ParticipantUID, UID


class DataManager:
    """Manage attribute names and IDs"""

    __participant_uid_offset: int
    """The first ParticipantUID"""
    __data_uid_offsets: list[int]
    """The first n-1 entries of this list are each the first AttributeValueUID of the corresponding attribute, the last entry is the first AttributeUID"""

    __data_uids: list[list[AttributeValueUID] | list[AttributeUID]]
    """A list containing a list per attribute,
          the inner lists contain the uid of the value each participant has in that attribute in order, the last entry of the outer list is a list of all attribute uids in order"""

    __uid_name_mapping: dict[UID, str]
    __name_uid_mapping: dict[tuple[str, AttributeUID], UID]

    def __map_value_name(
        self, uid: UID, attribute_uid: AttributeUID, name: str
    ) -> None:
        """Maps the uid of a given value of a given attribute to the name of the value"""
        self.__uid_name_mapping[uid] = copy(name)
        self.__name_uid_mapping[(name, attribute_uid)] = copy(uid)

    def __init__(self, data: list[list[str]]) -> None:
        """
        Initializer, stores the given data internally using uids.

        :param list[list[str]] data: A list containing a list per attribute,
          the inner lists contain the value each participant has in that attribute in order, the last entry of the outer list is a list of all attribute names in order
        """
        self.__data_uids = [[None] * len(data[0]) for _ in range(len(data) - 1)] + [
            [None] * len(data[-1])
        ]  # initialize __data_uids with correct lengths (should be the same as data)

        self.__data_uid_offsets = [None] * len(data)

        self.__name_uid_mapping = dict()
        self.__uid_name_mapping = dict()

        self.__data_uid_offsets[-1] = len(data[0]) * (len(data) - 1)
        self.__participant_uid_offset = self.__data_uid_offsets[-1] + len(data[-1])

        current_uid: UID = self.__data_uid_offsets[-1]
        for i in range(len(data[-1])):
            # self.__attribute_value_mapping[current_uid] = set()
            self.__uid_name_mapping[current_uid] = data[-1][i]
            self.__name_uid_mapping[(data[-1][i], -1)] = current_uid
            self.__data_uids[-1][i] = current_uid
            current_uid += 1

        current_uid = 0
        for i in range(len(data) - 1):
            self.__data_uid_offsets[i] = current_uid
            current_participant_uid: ParticipantUID = self.__participant_uid_offset
            for j in range(len(data[i])):
                if (
                    data[i][j],
                    self.__data_uid_offsets[-1] + i,
                ) not in self.__name_uid_mapping:
                    self.__map_value_name(
                        current_uid, self.__data_uid_offsets[-1] + i, data[i][j]
                    )
                    current_uid += 1

                self.__data_uids[i][j] = self.__name_uid_mapping[
                    (data[i][j], self.__data_uid_offsets[-1] + i)
                ]

                current_participant_uid += 1

    def get_values_by_attribute(self, uid: AttributeUID) -> set[AttributeValueUID]:
        """Returns a set containing all the uids of all the values the attribute with a given uid can have"""
        return set(self.__data_uids[uid - self.__data_uid_offsets[-1]])

    """
    def get_attribute_by_value(self, uid: AttributeValueUID) -> AttributeUID:
        return self.__value_attribute_mapping[uid]
    """

    def get_attribute_uid_by_name(self, name: str) -> AttributeUID:
        return self.__name_uid_mapping[(name, -1)]

    def get_value_uid_by_name_and_attribute(self, name: str, uid: AttributeUID):
        return self.__name_uid_mapping[(name, uid)]

    def get_name_by_uid(self, uid: UID) -> str:
        return self.__uid_name_mapping[uid]

    def get_value_by_participant(
        self, participant: ParticipantUID, attribute: AttributeUID
    ) -> AttributeValueUID:
        """Returns the uid of the value of the attribute of a given uid for the participant of a given uid"""
        return self.__data_uids[attribute - self.__data_uid_offsets[-1]][
            participant - self.__participant_uid_offset
        ]
