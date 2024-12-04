import openpyxl as opxl
from data_structures import Participant


class Reader:
    """class that reads excel sheets and turns the table into a list of participants"""

    __filepath: str

    def set_filepath(self, path: str) -> None:
        """sets the filepath to the given path in the reader"""
        self.__filepath = path

    def read(self) -> list[Participant]:
        """main read function, returns the parsed list of participants"""

        participant_list: list[Participant] = list()

        dataframe = opxl.load_workbook(self.__filepath)
        dataframe_active = dataframe.active

        header_list: dict[int, str] = dict()

        header_row = next(dataframe_active.rows)

        for i, entry in enumerate(header_row):
            header_list[i] = entry.value

        for i in range(2, dataframe_active.max_row):
            p: Participant = Participant(str(i))
            for j in range(0, dataframe_active.max_column):
                p.set_attribute(header_list[j], dataframe_active[i][j].value)

            participant_list.append(p)

        return participant_list
