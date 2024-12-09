"""Module for Excel tools."""

import os
from enum import Enum
import openpyxl as opxl
from openpyxl.styles import PatternFill


class FillColours(Enum):
    """Enum for some fill colours of openpyxl"""

    # pylint: disable=too-few-public-methods
    GREEN = PatternFill(start_color="00CCFFCC", fill_type="solid")
    VIOLET = PatternFill(start_color="00CC99FF", fill_type="solid")


def read_excel(path: os.PathLike, worksheet_name: str | None = None) -> list[list[str]]:
    """Read an Excel workbook

    :param path: Path to the Excel file to be read
    :param worksheet_name: Name of the worksheet to load or `None` to auto-select

    :return: A list of rows of the worksheet
    """

    workbook = opxl.load_workbook(path)
    worksheet: opxl.worksheet.worksheet.Worksheet
    if worksheet_name is None:
        worksheet = workbook.active
    else:
        worksheet = workbook.get_sheet_by_name(worksheet_name)

    # `worksheet.iter_rows(values_only=True)` yields rows in form of `tuple[str|None]`
    # so we convert them to `list[str]` and collect them in a list -> `list[list[str]]`
    return [
        [str(element) if not element is None else str() for element in row]
        for row in worksheet.iter_rows(values_only=True)
    ]


def write_excel(
    path: os.PathLike, data: list[list[str]], worksheet_name: str | None = None
) -> None:
    """Write data to an Excel file

    :param path: Path to write the Excel file to (will overwrite)
    :param data: List of rows of elements
    :param worksheet_name: Optional name for the new Worksheet
    """
    workbook = opxl.Workbook(write_only=True)
    workbook.create_sheet(worksheet_name)
    worksheet = workbook.active
    for row in data:
        worksheet.append(row)

    workbook.save(path)
