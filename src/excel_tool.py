"""Module for Excel tools."""

import os
from enum import Enum
import openpyxl as opxl
from openpyxl.styles import PatternFill
from data_structures import Participant, Assignment, ListOfRowLists
from data_structure_formatter import (
    str_matrix_to_participant_set,
    assignment_to_str_matrix,
)


class FillColours(Enum):
    """Enum for some fill colours of `openpyxl`."""

    # pylint: disable=too-few-public-methods
    GREEN = PatternFill(start_color="00CCFFCC", fill_type="solid")
    VIOLET = PatternFill(start_color="00CC99FF", fill_type="solid")


def read_excel(
    path: os.PathLike, worksheet_name: str | None = None
) -> ListOfRowLists[str]:
    """Read an Excel workbook.

    :param path: Path to the Excel file to be read
    :param worksheet_name: Name of the worksheet to load or `None` to auto-select

    :return: A list of rows of the worksheet
    """

    workbook = opxl.load_workbook(path)
    worksheet: opxl.worksheet.worksheet.Worksheet
    if worksheet_name is None:
        worksheet = workbook.active
    else:
        worksheet = workbook[worksheet_name]

    # `worksheet.iter_rows(values_only=True)` yields rows in form of `tuple[str|None]`
    # so we convert them to `list[str]` and collect them in a list -> `list[list[str]]`
    return [
        [str(element) if not element is None else str() for element in row]
        for row in worksheet.iter_rows(values_only=True)
    ]


def read_participant_set_excel(
    path: os.PathLike, worksheet_name: str | None = None
) -> set[Participant]:
    """Read a set of :class:`Participant`s from an Excel workbook.

    :param path: Path to he Excel file to be read
    :param worksheet_name: Name of the worksheet to load or `None` to auto-select

    :return: A set of :class:`Participant`s
    """
    return str_matrix_to_participant_set(read_excel(path, worksheet_name))


def write_excel(
    path: os.PathLike, data: ListOfRowLists[str], worksheet_name: str | None = None
) -> None:
    """Write data to an Excel file.

    :param path: Path to write the Excel file to (will overwrite)
    :param data: List of rows of elements
    :param worksheet_name: Optional name for the new Worksheet
    """
    workbook = opxl.Workbook()
    workbook.create_sheet(worksheet_name)
    worksheet = workbook.active
    for row in data:
        worksheet.append(row)

    # resize column widths
    # https://stackoverflow.com/a/39530676
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            # pylint: disable=broad-exception-caught
            try:  # Necessary to avoid error on empty cells
                max_length = max(max_length, len(str(cell.value)))
            except Exception:
                pass
        adjusted_width = (max_length + 2) * 1.0
        worksheet.column_dimensions[column].width = adjusted_width

    workbook.save(path)


def write_assignment_excel(
    path: os.PathLike, assignment: Assignment, worksheet_name: str | None = None
) -> None:
    """Write an :class:`Assignment` to an Excel file

    :param path: Path to write the Excel file to (will overwrite)
    :param assignment: :class:`Assignment` to write
    :param worksheet_name: Optional name for the new worksheet
    """
    write_excel(path, assignment_to_str_matrix(assignment), worksheet_name)
