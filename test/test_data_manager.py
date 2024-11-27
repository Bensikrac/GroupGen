from unittest import TestCase
from src.data_structures import AttributeUID, AttributeValueUID, ParticipantUID, UID
from src.data_manager import *


class TestDataManager(TestCase):

    data: list[list[str]]
    manager: DataManager

    def setUp(self) -> None:
        self.data = [
            ["andrew", "barbara", "clara", "dieter", "emil", "flora"],
            [
                "international",
                "deutsch",
                "international",
                "deutsch",
                "international",
                "international",
            ],
            ["10", "11", "8", "7", "10", "10"],
            ["name", "nationalität", "fachbereich"],
        ]
        self.manager = DataManager(self.data)

    def test_data_conservation(self):
        """Tests whether data can be fully and correctly reconstructed from the information stored by the manager"""
        data2: list[list[str]] = [
            [str()] * len(self.data[0]) for _ in range(len(self.data) - 1)
        ] + [[str()] * len(self.data[-1])]
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                data2[i][j] = self.manager.get_name_by_uid(
                    self.manager._DataManager__data_uids[i][j]
                )
        self.assertEqual(self.data, data2)

    def test_attribute_value_lists(self):
        """Tests whether the lists of present values for an attribute is correctly returned"""
        attribute: AttributeUID = self.manager.get_attribute_uid_by_name("name")
        values: set[str] = set(
            [
                self.manager.get_name_by_uid(i)
                for i in self.manager.get_values_by_attribute(attribute)
            ]
        )
        self.assertEqual(
            set(["andrew", "barbara", "clara", "dieter", "emil", "flora"]), values
        )

        attribute = self.manager.get_attribute_uid_by_name("nationalität")
        values = set(
            [
                self.manager.get_name_by_uid(i)
                for i in self.manager.get_values_by_attribute(attribute)
            ]
        )
        self.assertEqual(set(["deutsch", "international"]), values)

        attribute = self.manager.get_attribute_uid_by_name("fachbereich")
        values = set(
            [
                self.manager.get_name_by_uid(i)
                for i in self.manager.get_values_by_attribute(attribute)
            ]
        )
        self.assertEqual(set(["10", "11", "8", "7"]), values)
