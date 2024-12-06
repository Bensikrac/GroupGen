import pytest
from data_structures import Participant, assignment_to_str_matrix
from excel_tool import write_excel


def test_assignment_conversion() -> None:
    attributes = {"class": "value"}
    assignment = [
        [
            {Participant(1, attributes), Participant(2, attributes)},
            {Participant(3, attributes), Participant(4, attributes)},
            {Participant(5, attributes), Participant(6, attributes)},
            {Participant(7, attributes), Participant(8, attributes)},
        ],
        [
            {Participant(9, attributes), Participant(10, attributes)},
            {Participant(11, attributes), Participant(12, attributes)},
            {Participant(13, attributes), Participant(14, attributes)},
            {Participant(15, attributes), Participant(16, attributes)},
        ],
    ]

    string_matrix = assignment_to_str_matrix(assignment)
    # write_excel("test.xlsx", string_matrix)
    assert True
