from unittest.mock import patch
from app import MainWindow
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
)


def test_input_file_picker():
    app = QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    with patch.object(
        QFileDialog,
        "getOpenFileName",
        return_value=(
            "test_data/excel_reader_test_0.xlsx",
            "Excel Files (*.xlsx *.xls)",
        ),
    ):
        test_window._MainWindow__input_file_picker()
    assert (
        test_window.input_file_path_line_edit.text()
        == "test_data/excel_reader_test_0.xlsx"
    )
    assert test_window._MainWindow__input_path == ("test_data/excel_reader_test_0.xlsx")


def test_read_input_file():
    app = QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    assert test_window is not None
