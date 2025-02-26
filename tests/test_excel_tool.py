import os
import pytest
import excel_tool
from excel_tool import Reader, Writer
from data_structures import Participant
from data_structures import Assignment, Iteration, Group


def test_tool():
    list = Reader.read("test_data/excel_reader_test_0.xlsx")
    __output_path: os.PathLike = "test_data/excel_writer_test_0.xlsx"

    testobject1 = Participant(
        0,
        {
            "Angemeldet": "Ye",
            "Status": "Ne",
            "Form of address": "C2",
            "Title": "D3",
            "First name": "erster Name",
            "Last name": "Letzter Name ",
            "Personal-No. (TU employees only)": "4444",
            "Nationality": "Schweitz",
            "Email address": "nicht@meine.mail",
            "Telephone": "49000011122.56",
            "Department": "Physik",
            "Institute / Graduate School / Research Training Group": "TuDA",
        },
    )
    testobject2 = Participant(
        1,
        {
            "Angemeldet": "Non",
            "Status": "True",
            "Form of address": "False",
            "Title": "D3",
            "First name": "erster Name",
            "Last name": "F",
            "Personal-No. (TU employees only)": "G",
            "Nationality": "H",
            "Email address": "2020-05-17",
            "Telephone": "J",
            "Department": "K",
            "Institute / Graduate School / Research Training Group": "L",
        },
    )
    # Test first entry
    assert list[0].uid == testobject1.uid
    for attrib in [
        "Angemeldet",
        "Status",
        "Form of address",
        "First name",
        "Last name",
        "Personal-No. (TU employees only)",
        "Nationality",
        "Email address",
        "Telephone",
        "Department",
        "Institute / Graduate School / Research Training Group",
    ]:
        assert list[0].get_attribute(attrib) == testobject1.get_attribute(attrib)
    # Test second entry
    assert list[1].uid == testobject2.uid
    for attrib in [
        "Angemeldet",
        "Status",
        "Form of address",
        "First name",
        "Last name",
        "Personal-No. (TU employees only)",
        "Nationality",
        "Email address",
        "Telephone",
        "Department",
        "Institute / Graduate School / Research Training Group",
    ]:
        assert list[1].get_attribute(attrib) == testobject2.get_attribute(attrib)

    # Beginning off Writer Tests
    group1: Group = {testobject1, testobject1, testobject1}
    group2: Group = {testobject2, testobject2, testobject2}
    group3: Group = {testobject1, testobject1, testobject2}
    group4: Group = {testobject1, testobject2, testobject2}

    iter1: Iteration = [group1, group2]
    iter2: Iteration = [group3, group4]

    assign: Assignment = [iter1, iter2]

    Writer(__output_path).write_file(assign)

    # Now check if the groups and iterations match please


def test_errors():
    with pytest.raises(Exception):
        reader = excel_tool.Reader("/")
        reader.read()
