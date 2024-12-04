import pytest
import excel_tool
from data_structures import Participant


def test_file_read():
    reader = excel_tool.Reader("test_data/excel_reader_test_0.xlsx")
    list = reader.read()
    testobject1 = Participant(str(1),{'Angemeldet': 'Ye', 'Status': 'Ne', 'Form of address': 'C2', 'Title': 'D3', 'First name': 'erster Name', 'Last name': 'Letzter Name ', 'Personal-No. (TU employees only)': 4444, 'Nationality': 'Schweitz', 'Email address': 'nicht@meine.mail', 'Telephone': 49000011122, 'Department': 'Physik', 'Institute / Graduate School / Research Training Group': 'TuDA'})
    testobject2 = Participant(str(2),{'Angemeldet': 'Non', 'Status': 'TRUE', 'Form of address': 'FALSE', 'Title': 'D3', 'First name': 'erster Name', 'Last name': 'F', 'Personal-No. (TU employees only)': 'G', 'Nationality': 'H', 'Email address': 'I', 'Telephone': 'J', 'Department': 'K', 'Institute / Graduate School / Research Training Group': 'L'})
    # Test first entry
    assert list[0].get_name() == testobject1.get_name()
    for attrib in ['Angemeldet', 'Status', 'Form of address', 'First name', 'Last name','Personal-No. (TU employees only)', 'Nationality', 'Email address', 'Telephone', 'Department', 'Institute / Graduate School / Research Training Group']:
        assert list[0].get_attribute(attrib) == testobject1.get_attribute(attrib)
    # Test second entry
    assert list[1].get_name() == testobject2.get_name()
    for attrib in ['Angemeldet', 'Status', 'Form of address', 'First name', 'Last name','Personal-No. (TU employees only)', 'Nationality', 'Email address', 'Telephone', 'Department', 'Institute / Graduate School / Research Training Group']:
        assert list[1].get_attribute(attrib) == testobject1.get_attribute(attrib)

def test_change_path():
    reader = excel_tool.Reader("/")
    reader.set_filepath("test_data/excel_reader_test_0.xlsx")
    assert reader.read() != None


def test_errors():
    with pytest.raises(Exception):
        reader = excel_tool.Reader("/")
        reader.read()