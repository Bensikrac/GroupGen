"""Module containing tests for app.py."""

from unittest.mock import patch

import pytest
from app import MainWindow
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
)

from excel_tool import Writer


def test_input_file_picker():
    """Tests if the imput file picker correctly sets the file path internally and visually."""
    app = QApplication.instance() or QApplication(sys.argv)
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


def test_output_file_picker():
    """Tests if the output file picker correctly sets the file path internally and visually."""
    app = QApplication.instance() or QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    with patch.object(
        QFileDialog,
        "getSaveFileName",
        return_value=(
            "test_data/test_output",
            "Excel Files (*.xlsx *.xls)",
        ),
    ):
        test_window._MainWindow__output_file_picker()
    assert test_window.output_file_path_line_edit.text() == "test_data/test_output.xlsx"
    assert test_window._MainWindow__output_path == ("test_data/test_output.xlsx")


def test_read_input_file():
    """Tests if read_input_file reads the correct number of entries into the participant list and sets the status."""
    app = QApplication.instance() or QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    test_window._MainWindow__input_path = "test_data/excel_reader_test_0.xlsx"
    test_window._MainWindow__read_input_file()

    assert len(test_window._MainWindow__participants_list) == 2
    assert test_window.state_label.text() == "Status: Finished Reading..."


def test_run_workflow():
    """Tests if run_workflow runs without issue and sets the status correctly."""
    app = QApplication.instance() or QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    test_window._MainWindow__input_path = "test_data/test_data_short_1.xlsx"
    test_window._MainWindow__output_path = "test_data/test_output.xlsx"
    test_window._MainWindow__read_input_file()
    test_window.groups_spinbox.setValue(2)
    test_window.iterations_spinbox.setValue(2)

    with patch.object(Writer, "write_file", return_value=None):
        test_window._MainWindow__run_workflow()
    assert test_window.state_label.text() == "Status: Finished!"


def test_run_workflow_path_errors():
    """Tests if run_workflow handles missing paths correctly."""
    app = QApplication.instance() or QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    test_window._MainWindow__output_path = "test_data/test_output.xlsx"
    with pytest.raises(ValueError) as error:
        test_window._MainWindow__run_workflow()
    assert "Input Path not set" in str(error.value)

    test_window_2: MainWindow = MainWindow("assets/main_window.ui")
    test_window_2._MainWindow__input_path = "test_data/test_data_short_1.xlsx"
    with pytest.raises(ValueError) as error:
        test_window_2._MainWindow__run_workflow()
    assert "Output Path not set" in str(error.value)
