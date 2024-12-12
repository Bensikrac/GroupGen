"""Module which handles reading and writing of excel files"""

import os
import openpyxl as opxl
from data_structures import Participant


class Reader:
    """class that reads excel sheets and turns the table into a list of participants"""

    __filepath: os.PathLike

    def __init__(self, path: os.PathLike) -> None:
        """create a new reader with the given path

        :param path: filepath used for reading the excel sheet
        """
        self.__filepath = path

    def read(self) -> list[Participant]:
        """main read function, returns the parsed list of participants

        :return: a list of Participants found in the excel file with teir attributes
        """

        participant_list: list[Participant] = []

        dataframe = opxl.load_workbook(self.__filepath)
        dataframe_active = dataframe.active

        header_list: dict[int, str] = {}

        header_row = next(dataframe_active.rows)

        for i, entry in enumerate(header_row):
            header_list[i] = entry.value

        for i in range(2, dataframe_active.max_row):
            p: Participant = Participant(i)

            for j in range(0, dataframe_active.max_column):
                p.set_attribute(header_list[j], dataframe_active[i][j].value)

            participant_list.append(p)

        return participant_list
