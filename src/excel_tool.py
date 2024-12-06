import os
import openpyxl as opxl


def read_excel(path: os.PathLike, worksheet_name: str | None = None) -> list[list[str]]:
    """Read an Excel workbook

    :param path: Path to the Excel file to be read
    :param worksheet_name: Name of the worksheet to load or `None` to auto-select

    :return: A list of rows of the worksheet
    """

    workbook = opxl.load_workbook(path)
    worksheet: opxl.Worksheet
    if worksheet_name is None:
        worksheet = workbook.active
    else:
        worksheet = workbook.get_sheet_by_name(worksheet_name)

    retval: list[list[str]] = []

    for i in range(worksheet.max_row):
        retval.append([])
        for j in range(worksheet.max_column):
            retval[i].append(str(worksheet.cell(i, j)))

    return retval


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
    for i, row in enumerate(data):
        for j, element in enumerate(row):
            worksheet.cell(i, j, element)

    workbook.save(path)
