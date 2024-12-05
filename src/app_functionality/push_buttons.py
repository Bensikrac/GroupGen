from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog

from excel_tool import Reader


def file_picker() -> None:
    """The function to pick files and import the excel sheet"""

    __filepath: str = QFileDialog.getOpenFileName(
        caption="pick file", directory="/home", filter="Excel Files (*.xls *.xlsx)"
    )[0]
    excel_reader: Reader = Reader(__filepath)

    if __filepath != "":
        excel_reader.read()
