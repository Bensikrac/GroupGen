import pytest
import excel_tool as excel_tool
from data_structures import Participant


def test_file_read():
    reader = excel_tool.Reader("test_data/excel_reader_test_0.xlsx")
    list = reader.read()
    testobject1 = Participant(
        1,
        {
            "Angemeldet": "Ye",
            "Status": "Ne",
            "Form of address": "C2",
            "Title": "D3",
            "First name": "erster Name",
            "Last name": "Letzter Name ",
            "Personal-No. (TU employees only)": 4444,
            "Nationality": "Schweitz",
            "Email address": "nicht@meine.mail",
            "Telephone": 49000011122,
            "Department": "Physik",
            "Institute / Graduate School / Research Training Group": "TuDA",
        },
    )
    testobject2 = Participant(
        2,
        {
            "Angemeldet": "Non",
            "Status": True,
            "Form of address": False,
            "Title": "D3",
            "First name": "erster Name",
            "Last name": "F",
            "Personal-No. (TU employees only)": "G",
            "Nationality": "H",
            "Email address": "I",
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


def test_errors():
    with pytest.raises(Exception):
        reader = excel_tool.Reader("/")
        reader.read()
