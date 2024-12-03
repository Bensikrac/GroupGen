import openpyxl as opxl
from openpyxl.styles import PatternFill
from data_structures import Participant

import os


class Reader:
    """class that reads excel sheets and turns the table into a list of participants"""

    __filepath: str

    def __init__(self, path: str) -> None:
        """create a new reader with the given file path. the path can be absolute or reltive"""
        self.__filepath = path

    def set_filepath(self, path: str) -> None:
        """sets the filepath to the given path in the reader"""
        __filepath = path

    def read(self) -> list[Participant]:
        """main read function, returns the parsed list of participants"""

        participant_list: list[Participant] = list()

        dataframe = opxl.load_workbook(self.__filepath)
        dataframe_active = dataframe.active

        header_list: dict[int, str] = dict()

        header_row = next(dataframe_active.rows)

        for i, entry in enumerate(header_row):
            header_list[i] = entry.value

        for i in range(1, dataframe_active.max_row):
            p: Participant = Participant(str(i))
            for j in range(0, dataframe_active.max_column):
                p.set_attribute(header_list[j], dataframe_active[i][j].value)

            participant_list.append(p)

        return participant_list

class Writer():
    """Class that writes excel sheet and turns calculated groups in an understandable format."""
    
    __filepath: os.PathLike

    @classmethod
    def set_filepath(cls, filepath: os.PathLike) -> None:
        """This method is used to set filepath of resulting excel sheet.
        
        :param filepath: filepath set used for writing the excle sheet.
        """
        cls.__filepath = filepath

    @classmethod
    def write_file(cls, groupset: list[list[set[Participant]]]) -> None:
        """This method is used to write the excel sheet to the path that is set containing the iterations with its groups.

        :param groupset: The groups generated for each iteration (form: iterations[groups[set of participants]])
        """

        __row_index: int = 1
        __attribute_list: list = [key for key in next(iter(groupset[0][0])).attributes.keys()]

        #Colors for coloring the first cell for better understandability 
        __green_fill: PatternFill = PatternFill(start_color="00CCFFCC", fill_type= "solid")
        __violet_fill: PatternFill = PatternFill(start_color="00CC99FF", fill_type= "solid")

        wb = opxl.Workbook()
        ws = wb.worksheets[0]

        for iteration_index in range(len(groupset)):
            # for-loop for iterations of the algorithm
            ws.cell(__row_index, 1).value = f"Iteration {iteration_index + 1}:"
            __row_index += 1
            ws.cell(__row_index, 1).value = "GroupNr"
            for group_index in range(len(__attribute_list)):
                ws.cell(__row_index, 2 + group_index).value = __attribute_list[group_index]

            # head-row of each iteration of algorithm 

            __row_index += 1

            for group_index in range(len(groupset[iteration_index])):
                # for-loop groups of an iteration of algorithm
                group_iter = iter(groupset[iteration_index][group_index])
                
                
                for participant in group_iter:
                    ws.cell(__row_index, 1).value = group_index+1 #Group numbers should start with 1

                    ws.cell(__row_index, 1).fill = __green_fill if group_index % 2 == 1 else __violet_fill #coloring cells

                    for attribute_iterator in range(len(__attribute_list)):
                        ws.cell(__row_index, 2 + attribute_iterator).value = participant.get_attribute(__attribute_list[attribute_iterator])
                    __row_index +=1
                #groups of Iteration written
                
            __row_index += 2 #add 2 extra empty rows for better readability

        wb.save(cls.__filepath)
