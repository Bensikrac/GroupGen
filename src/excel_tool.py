"""Module which handles reading and writing of excel files"""

import os
import openpyxl as opxl
from openpyxl.styles import PatternFill
import python_calamine
from data_structures import Participant, Group, Iteration, Assignment


def read_calamine(filepath: os.PathLike) -> list[Participant]:
    """Reads an excel file on the speciefied location and creates a list of participants from it.

    :param filepath: The path to the file to be read
    :return: The list of participants with initialized attributes"""
    workbook = python_calamine.CalamineWorkbook.from_path(filepath)
    rows = iter(workbook.get_sheet_by_index(0).to_python())

    headers = list(map(str, next(rows)))

    participant_list: list[Participant] = []
    j: int = 0

    for row in rows:
        p: Participant = Participant(j)

        # All dates will be represented in the following form: 2025-01-31
        for i in range(0, len(headers)):
            if isinstance(row[i], float) and row[i].is_integer():
                p.attributes[headers[i]] = f"{row[i]:.0f}"
            else:
                p.attributes[headers[i]] = str(row[i])

        participant_list.append(p)
        j += 1

    return participant_list


class Writer:
    """Class that writes excel sheet and turns calculated groups in an understandable format.
    Only meant to be used once. Object of Writer should only be present when writing file
    """

    # Colors for coloring the first cell for better understandability
    __fill_colors: tuple[PatternFill] = (
        PatternFill(start_color="00CCFFCC", fill_type="solid"),  # green
        PatternFill(start_color="00CC99FF", fill_type="solid"),  # violet
    )

    def __init__(self, filepath: os.PathLike) -> None:
        self.__filepath = filepath

    def __write_header(
        iteration_number: int, attribute_list: list[str], ws, row_index
    ) -> None:
        """This function writes the header for an iteration with the iteration number and
        header row(group, list of attributes).

        :param iteration_number: number of the iteration to be written
        :param attribute_list: list of attribute names of participants
        :param row_index: row index to be written to
        :param ws: worksheet to be written on
        """

        ws.cell(row_index, 1).value = f"Iteration {iteration_number}:"

        ws.cell(row_index + 1, 1).value = "GroupNr"

        for i, attribute in enumerate(attribute_list):
            ws.cell(row_index + 1, 2 + i).value = attribute

    def __write_participant(
        participant: Participant,
        group_number: int,
        attribute_list: list[str],
        ws,
        row_index: int,
    ) -> None:
        """This function writes a participant with its group number (colored background) and
        its attribute values.

        :param participant: participant to be written
        :param group_number: group number of the participant
        :param attribute_list: list of attribute names of participants
        :param ws: worksheet to be written to
        """

        ws.cell(row_index, 1).fill = Writer.__fill_colors[
            group_number % len(Writer.__fill_colors)
        ]

        ws.cell(row_index, 1).value = group_number

        for i, attribute in enumerate(attribute_list):
            ws.cell(row_index, 2 + i).value = participant.get_attribute(attribute)

    def __write_group(
        group: Group, group_number: int, attribute_list: list[str], ws, row_index: int
    ) -> int:
        """This function writes all members of a group to the worksheet.

        :param group: group to be written
        :param group_number: group number of the group
        :param attribute_list: list of attribute names of participants
        :param ws: worksheet to be written to
        """

        for participant in iter(group):
            Writer.__write_participant(
                participant, group_number, attribute_list, ws, row_index
            )
            row_index += 1
        return row_index

    def __write_iteration(
        iteration: Iteration,
        iteration_number: int,
        attribute_list: list[str],
        ws,
        row_index: int,
    ) -> int:
        """This function writes the iteration header and paricipants of all groups to the worksheet.

        :param iteration: iteration to be written
        :param iteration_number: number of the iteration that is written
        :param attribute_list: list of attribute names of participants
        :param ws: worksheet to be written to
        """

        # write iteration
        Writer.__write_header(iteration_number, attribute_list, ws, row_index)

        row_index += 2

        for i, group in enumerate(iteration):
            row_index = Writer.__write_group(
                group, i + 1, attribute_list, ws, row_index
            )

        return row_index + 2  # add 2 extra empty rows for better readability

    def __write_assignment(assignment: Assignment, ws) -> None:
        """This function writes an assignment with all its iteration.

        :param assignment: assignment to be printed
        :param row_index: row index to be written to
        :param ws: worksheet to be written to
        """
        row_index: int = 1

        attribute_list: list[str] = list(next(iter(assignment[0][0])).attributes.keys())

        for i, iteration in enumerate(assignment):
            row_index = Writer.__write_iteration(
                iteration, i + 1, attribute_list, ws, row_index
            )

    def write_file(assignment: Assignment, filepath: os.PathLike) -> None:
        """This method is used to write the excel sheet to the path that is set containing
        the iterations with its groups.

        :param assignment: The assignment to be written to the excel file
        """

        wb = opxl.Workbook()
        ws = wb.worksheets[0]

        Writer.__write_assignment(assignment, ws)

        wb.save(filepath)
