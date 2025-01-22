"""Main app to be launched"""

import copy
from operator import itemgetter
import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
)
from PyQt6.QtCore import QRect, QModelIndex
from excel_tool import Reader, Writer
from data_structures import Participant, Assignment
from algorithm.simulated_annealing_algorithm import SimulatedAnnealingAlgorithm
from ui.attribute_table_items import CheckableHeaderItem

type HistoryState = list[list[str]]


class MainWindow(QMainWindow):
    """Main Window class.

    Takes args and kwargs like :class:`QMainWindow`.
    """

    # pylint: disable=too-few-public-methods

    __input_path: os.PathLike | None = None
    __output_path: os.PathLike | None = None
    __participants_list: list[Participant]
    __attributes_list: list[str]
    __history: list[HistoryState] = [[]]
    __history_index: int = 0

    def __init__(self, ui_file_path: os.PathLike, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        uic.loadUi(ui_file_path, self)

        self.attributes_table.set_main_window(self)

        self.setWindowTitle("GroupGen")

        self.input_pick_button.clicked.connect(self.__input_file_picker)
        # self.read_input_button.clicked.connect(self.__read_input_file)
        self.output_pick_button.clicked.connect(self.__output_file_picker)
        self.run_algorithm_button.clicked.connect(self.__run_algorithm)
        # self.select_synonym_button.clicked.connect()
        self.reset_synonyms_button.clicked.connect(self.__reset_synonyms)
        self.undo_button.clicked.connect(self.__undo)
        self.redo_button.clicked.connect(self.__redo)

        # self.read_input_button.setEnabled(False)
        self.run_algorithm_button.setEnabled(False)
        # self.select_synonym_button.setEnabled(False)
        self.select_synonym_label.setVisible(False)
        self.undo_button.setEnabled(False)
        self.redo_button.setEnabled(False)
        self.reset_synonyms_button.setEnabled(False)

    def __run_algorithm(self) -> None:
        """Executes the algorithm and and writes the output."""
        if self.__input_path is None:
            raise ValueError("Input Path not set")
        if self.__output_path is None:
            raise ValueError("Output Path not set")

        self.state_label.setText("Status: Preparing...")
        self.state_label.repaint()

        algorithm_instance: SimulatedAnnealingAlgorithm = SimulatedAnnealingAlgorithm(
            self.__filter_enabled_attributes()
        )

        self.state_label.setText("Status: Calculating...")
        self.state_label.repaint()

        final_assignment: Assignment = algorithm_instance.find_assignment(
            self.__synonym_filter_participants(),
            int(self.groups_spinbox.value()),
            int(self.iterations_spinbox.value()),
            1000,
        )

        Writer(self.__output_path).write_file(final_assignment)

        self.state_label.setText("Status: Finished!")
        self.state_label.repaint()

    def __synonym_filter_participants(self) -> set[Participant]:
        """Returns a set of partcicpants that are each equivalent to one of the stored participants,
        but have all attribute values replaced with their preferred synonyms.

        :return: A set containing the filtered participants
        """
        filtered_participants: set[Participant] = set()
        for participant in self.__participants_list:
            attributes: dict[str, str] = {}
            for attribute in participant.attributes:
                attributes[attribute] = self.attributes_table.find_preferred_synonym(
                    participant.get_attribute(attribute)
                )
            # filtered_participants.add(Participant(attributes))
            filtered_participants.add(Participant(participant.get_uid(), attributes))
        return filtered_participants

    def __input_file_picker(self) -> None:
        """Select Input File Button Function"""
        self.__input_path = QFileDialog.getOpenFileName(
            caption="pick file", directory="/home", filter="Excel Files (*.xlsx *.xls)"
        )[0]
        self.input_file_path_line_edit.setText(self.__input_path)
        self.input_file_path_line_edit.repaint()

        # self.read_input_button.setEnabled(True)
        self.__read_input_file()

    def __read_input_file(self) -> None:
        """Read Input File Button Function"""

        self.state_label.setText("Status: Reading...")
        self.state_label.repaint()
        self.__set_buttons_enabled(False)

        self.__participants_list = Reader(self.__input_path).read()
        self.__attributes_list = self.__participants_list[0].attributes.keys()

        # Construct Table
        self.attributes_table.synonyms = []
        self.construct_attribute_table()

        self.state_label.setText("Status: Finished Reading...")
        self.state_label.repaint()
        self.select_synonym_label.setVisible(True)
        self.__set_buttons_enabled(True)
        self.__update_undo_redo()

    def __reset_synonyms(self) -> None:
        """Reset Synonyms button function."""
        self.attributes_table.synonyms = []
        self.add_state_to_history([])
        self.construct_attribute_table()

    def __undo(self) -> None:
        """Move back one step in the history."""
        if self.__history_index > 0:
            self.__history_index -= 1
            self.__step_to_history_state(self.__history_index)
            self.construct_attribute_table()
        self.__update_undo_redo()

    def __redo(self) -> None:
        """Move forward one step in the history."""
        if self.__history_index < len(self.__history) - 1:
            self.__history_index += 1
            self.__step_to_history_state(self.__history_index)
            self.construct_attribute_table()
        self.__update_undo_redo()

    def __update_undo_redo(self) -> None:
        """Set the undo and redo buttons as enabled or disabled appropriately."""
        self.undo_button.setEnabled(self.__history_index > 0)
        self.redo_button.setEnabled(self.__history_index < len(self.__history) - 1)

    def __step_to_history_state(self, state_index: int) -> None:
        """Change the state of the table and data to match the given state.

        :param state: The state to step into
        """
        state = self.__history[state_index]
        if isinstance(state, list):
            self.attributes_table.synonyms = copy.deepcopy(state)

    def add_state_to_history(self, state: HistoryState) -> None:
        """Add a state to the end of the history and deal with redunndant entries if appropriate.

        :param state: The state to add
        """
        self.__history = self.__history[: self.__history_index + 1]
        self.__history_index += 1
        self.__history.append(state)

        self.__update_undo_redo()

    def __output_file_picker(self) -> None:
        """Select Output File Button Function"""
        self.__output_path = QFileDialog.getSaveFileName(
            caption="pick file",
            directory="/home",
            filter="Excel Files (*.xlsx *.xls)",
        )[0]
        if not (
            self.__output_path.endswith(".xlsx") or self.__output_path.endswith(".xls")
        ):
            self.__output_path += ".xlsx"
        self.output_file_path_line_edit.setText(self.__output_path)

        self.run_algorithm_button.setEnabled(True)

    def construct_attribute_table(self) -> None:
        """Construct Attribute Table"""
        self.attributes_table.clearContents()
        self.attributes_table.setColumnCount(len(self.__attributes_list))
        # self.attributes_table.setHorizontalHeaderLabels(self.__attributes_list)

        max_row_count: int = 0
        for j, attrbutes in enumerate(self.__attributes_list):
            should_be_checked: bool = (
                attrbutes.lower()
                not in [
                    "name",
                    "first name",
                    "last name",
                    "vorname",
                    "nachname",
                    "angemeldet",
                    "status",
                    "title",
                    "titel",
                ],
            )

            self.attributes_table.setHorizontalHeaderItem(
                j,
                CheckableHeaderItem(attrbutes, should_be_checked),
            )

            unique_attributes: list[tuple[str, int]] = self.__calculate_distribution(
                self.__participants_list, attrbutes
            )

            if max_row_count < len(unique_attributes):
                max_row_count = len(unique_attributes)
                self.attributes_table.setRowCount(max_row_count)

            for i, (attr, nmb) in enumerate(unique_attributes):
                self.attributes_table.set_value(i, j, attr, nmb)

            self.attributes_table.repaint()

    def __filter_enabled_attributes(self) -> list[str]:
        enabled_attributes: list[str] = []
        for i in range(len(self.__attributes_list)):
            item: QTableWidgetItem = self.attributes_table.horizontalHeaderItem(i)
            if isinstance(item, CheckableHeaderItem) and item.checked:
                enabled_attributes.append(list(self.__attributes_list)[i])
                print(enabled_attributes)
        return enabled_attributes

    def __set_buttons_enabled(self, enable: bool) -> None:
        """Enable/Disable all Buttons of the Main Window

        :param enable: if true all Buttons are enabled, if false all Buttons are disabled
        """
        self.input_pick_button.setEnabled(enable)
        # self.read_input_button.setEnabled(enable)
        self.output_pick_button.setEnabled(enable)
        self.run_algorithm_button.setEnabled(enable)
        # self.select_synonym_button.setEnabled(enable)
        self.undo_button.setEnabled(enable)
        self.redo_button.setEnabled(enable)
        self.reset_synonyms_button.setEnabled(enable)

    def __calculate_distribution(
        self, participants: list[Participant], attribute: str
    ) -> list[tuple[str, int]]:
        """Returns a list of values for the given attribute and how often each value appears.

        :param: participants: The list of participants to search in
        :param: attribute: The attribute to find values for

        :return: A list of tuples, each containing a value and how many times it appears.
        """
        result: list[tuple[str, int]] = []
        for participant in participants:
            attribute_value: str = participant.get_attribute(attribute)
            if not attribute_value:
                continue
            found_synonym: bool = False
            old_entry: tuple[str, int]
            new_entry: tuple[str, int]
            for old_entry in result:
                if old_entry[0] == self.attributes_table.find_preferred_synonym(
                    attribute_value
                ):
                    new_entry = (old_entry[0], old_entry[1] + 1)
                    found_synonym = True
                    break
            if not found_synonym:
                result.append(
                    (self.attributes_table.find_preferred_synonym(attribute_value), 1)
                )
            else:
                result.remove(old_entry)
                result.append(new_entry)

        return sorted(result, key=itemgetter(0))


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow
    if len(sys.argv) < 2:
        window = MainWindow("assets/main_window.ui")
    else:
        window = MainWindow(*sys.argv[1:])
    window.show()

    app.exec()
