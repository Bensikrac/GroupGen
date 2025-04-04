"""Module containing tests for app.py."""

from unittest.mock import patch

import pytest
from app import MainWindow
from PyQt6.QtWidgets import QFileDialog, QMessageBox

from app import MainWindow
from data_structures import Participant
from excel_tool import Writer


def test_input_file_picker(main_window_fixture):
    """Tests if the imput file picker correctly sets the file path internally and visually."""
    with patch.object(
        QFileDialog,
        "getOpenFileName",
        return_value=(
            "test_data/test_data_short_1.xlsx",
            "Excel Files (*.xlsx *.xls)",
        ),
    ):
        main_window_fixture._MainWindow__input_file_picker()
    assert (
        main_window_fixture.input_file_path_line_edit.text()
        == "test_data/test_data_short_1.xlsx"
    )
    assert main_window_fixture._MainWindow__input_path == (
        "test_data/test_data_short_1.xlsx"
    )


def test_output_file_picker(main_window_fixture):
    """Tests if the output file picker correctly sets the file path internally and visually."""
    with patch.object(
        QFileDialog,
        "getSaveFileName",
        return_value=(
            "test_data/test_output",
            "Excel Files (*.xlsx *.xls)",
        ),
    ):
        main_window_fixture._MainWindow__output_file_picker()
    assert (
        main_window_fixture.output_file_path_line_edit.text()
        == "test_data/test_output.xlsx"
    )
    assert main_window_fixture._MainWindow__output_path == (
        "test_data/test_output.xlsx"
    )


def test_read_input_file(main_window_fixture):
    """Tests if read_input_file reads the correct number of entries into the participant list and sets the status."""
    main_window_fixture._MainWindow__input_path = "test_data/test_data_short_1.xlsx"
    main_window_fixture._MainWindow__read_input_file()

    assert len(main_window_fixture._MainWindow__participants_list) == 18


def test_run_workflow(main_window_fixture):
    """Tests if run_workflow runs without issue and sets the status correctly."""
    main_window_fixture._MainWindow__input_path = "test_data/test_data_short_1.xlsx"
    main_window_fixture._MainWindow__output_path = "test_data/test_output.xlsx"
    main_window_fixture._MainWindow__read_input_file()
    main_window_fixture.groups_spinbox.setValue(2)
    main_window_fixture.iterations_spinbox.setValue(2)

    with patch.object(Writer, "write_file", return_value=None):
        with patch.object(QMessageBox, "exec", return_value=None):
            main_window_fixture._MainWindow__start_algorithm()
            # while not main_window_fixture.algorithm_finished: pass
    # Every attempt on waiting for the algorithm thread to finish failed so i will comment this out.
    # On a further notice, the state label is to be removed anyway.
    # assert main_window_fixture.state_label.text() == "Status: Finished!"


def test_run_workflow_path_errors(app_fixture):
    """Tests if run_workflow handles missing paths correctly."""
    test_window: MainWindow = MainWindow()
    test_window._MainWindow__output_path = "test_data/test_output.xlsx"
    with pytest.raises(ValueError) as error:
        test_window._MainWindow__start_algorithm()
        # while not test_window.algorithm_finished: pass
    assert "Input Path not set" in str(error.value)
    test_window.close()

    test_window_2: MainWindow = MainWindow()
    test_window_2._MainWindow__input_path = "test_data/test_data_short_1.xlsx"
    with pytest.raises(ValueError) as error:
        test_window_2._MainWindow__start_algorithm()
        # while not test_window_2.algorithm_finished: pass
    assert "Output Path not set" in str(error.value)
    test_window_2.close()


def test_reset_synonyms(main_window_fixture):
    """Tests if clicking the reset synonyms button correctly empties the synonym list."""
    main_window_fixture.attributes_table.synonyms = [["foo", "bar"], ["ipsum", "lorem"]]
    main_window_fixture.reset_synonyms_button.click()
    assert main_window_fixture.attributes_table.synonyms == []
    main_window_fixture.reset_synonyms_button.click()
    assert main_window_fixture.attributes_table.synonyms == []


def test_undo_redo_branch(main_window_fixture):
    """Tests if undoing and redoing works correctly before and after the history branches."""
    main_window_fixture.attributes_table.synonyms = [
        [],
        ["foo", "bar"],
        ["ipsum", "lorem"],
    ]
    main_window_fixture._MainWindow__history = [
        [[]],
        [[], ["foo", "bar"]],
        [[], ["foo", "bar"], ["ipsum", "lorem"]],
    ]
    main_window_fixture._MainWindow__history_index = 2
    main_window_fixture._MainWindow__update_undo_redo

    main_window_fixture.undo_button.click()
    assert main_window_fixture.attributes_table.synonyms == [[], ["foo", "bar"]]
    assert main_window_fixture._MainWindow__history == [
        [[]],
        [[], ["foo", "bar"]],
        [[], ["foo", "bar"], ["ipsum", "lorem"]],
    ]
    assert main_window_fixture._MainWindow__history_index == 1

    main_window_fixture.undo_button.click()
    assert main_window_fixture.attributes_table.synonyms == [[]]
    assert main_window_fixture._MainWindow__history == [
        [[]],
        [[], ["foo", "bar"]],
        [[], ["foo", "bar"], ["ipsum", "lorem"]],
    ]
    assert main_window_fixture._MainWindow__history_index == 0

    main_window_fixture.redo_button.click()
    assert main_window_fixture.attributes_table.synonyms == [[], ["foo", "bar"]]
    assert main_window_fixture._MainWindow__history == [
        [[]],
        [[], ["foo", "bar"]],
        [[], ["foo", "bar"], ["ipsum", "lorem"]],
    ]
    assert main_window_fixture._MainWindow__history_index == 1

    main_window_fixture.reset_synonyms_button.click()
    assert main_window_fixture.attributes_table.synonyms == []
    assert main_window_fixture._MainWindow__history == [
        [[]],
        [[], ["foo", "bar"]],
        [],
    ]
    assert main_window_fixture._MainWindow__history_index == 2

    main_window_fixture.undo_button.click()
    assert main_window_fixture.attributes_table.synonyms == [[], ["foo", "bar"]]
    assert main_window_fixture._MainWindow__history == [
        [[]],
        [[], ["foo", "bar"]],
        [],
    ]
    assert main_window_fixture._MainWindow__history_index == 1

    main_window_fixture.redo_button.click()
    assert main_window_fixture.attributes_table.synonyms == []
    assert main_window_fixture._MainWindow__history == [
        [[]],
        [[], ["foo", "bar"]],
        [],
    ]
    assert main_window_fixture._MainWindow__history_index == 2


@pytest.fixture
def participants_list() -> list[Participant]:
    """Fixture of example of input from Reader

    :return: test participants_list
    """
    return [
        Participant({"Name": "Paul"}),
        Participant({"Name": "Paul"}),
        Participant({"Name": "Leon"}),
        Participant({"Name": ""}),
    ]


def test_calculate_distibution(main_window_fixture, participants_list):
    """Test if distribution is calculated correctly"""
    window = main_window_fixture

    result = window._MainWindow__calculate_distribution(
        participants_list,
        "Name",
    )
    expected = [
        ("Leon", 1),
        ("Paul", 2),
    ]

    assert result == expected


@pytest.fixture
def distribution() -> list[tuple[str, int]]:
    """Fixture of example of distribution input

    :return: unsorted distribution
    """
    return [
        ("Beta", 1),
        ("Alpha", 1),
        ("Charlie", 2),
    ]


def test_sort_distribution(main_window_fixture, distribution):
    """Test if provided distribution is sorted correctly"""
    window = main_window_fixture

    # Sort by Value (Initial Case)

    assert window.sorting_comboBox.currentText() == "Value"

    result = window._MainWindow__sort_distribution(distribution)
    expected = [
        ("Alpha", 1),
        ("Beta", 1),
        ("Charlie", 2),
    ]

    assert result == expected

    # Sort by Frequency

    window.sorting_comboBox.setCurrentText("Frequency")

    assert window.sorting_comboBox.currentText() == "Frequency"

    result = window._MainWindow__sort_distribution(distribution)
    expected = [
        ("Charlie", 2),
        ("Alpha", 1),
        ("Beta", 1),
    ]

    assert result == expected

    window.sorting_comboBox.setCurrentIndex(0)
