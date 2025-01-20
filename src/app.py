"""Main app to be launched"""

import copy
import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QCheckBox,
)
from PyQt6.QtCore import QRect, QModelIndex
from excel_tool import Reader, Writer
from data_structures import Participant, Assignment
from algorithm.simulated_annealing_algorithm import SimulatedAnnealingAlgorithm


class MainWindow(QMainWindow):
    """Main Window class"""

    # pylint: disable=too-few-public-methods

    __input_path: os.PathLike | None = None
    __output_path: os.PathLike | None = None
    __participants_list: list[Participant]
    __attributes_list: list[str]
    __checkboxes: list[QCheckBox] = []
    __history: list[list[list[str]] | QCheckBox] = [[]]
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
        self.__synonym_filter_participants()

        self.state_label.setText("Status: Calculating...")
        self.state_label.repaint()

        final_assignment: Assignment = algorithm_instance.find_assignment(
            set(self.__participants_list),
            int(self.groups_spinbox.value()),
            int(self.iterations_spinbox.value()),
            1000,
        )

        Writer(self.__output_path).write_file(final_assignment)

        self.state_label.setText("Status: Finished!")
        self.state_label.repaint()

    def __synonym_filter_participants(self) -> None:
        """Replaces all attribute values of all Participants with their preferred synonyms."""
        for participant in self.__participants_list:
            for attribute in participant.attributes:
                participant.set_attribute(
                    attribute,
                    self.attributes_table.find_preferred_synonym(
                        participant.get_attribute(attribute)
                    ),
                )

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

        # Print Table
        self.attributes_table.synonyms = []
        for checkbox in self.__checkboxes:
            checkbox.deleteLater()
        self.__checkboxes = []
        self.print_attribute_table()

        self.state_label.setText("Status: Finished Reading...")
        self.state_label.repaint()
        self.select_synonym_label.setVisible(True)
        self.__set_buttons_enabled(True)
        self.__update_undo_redo()

    def __reset_synonyms(self) -> None:
        """Reset Synonyms button function."""
        self.attributes_table.synonyms = []
        self.add_state_to_history([])
        self.print_attribute_table()

    def __undo(self) -> None:
        """Move back one step in the history."""
        if self.__history_index > 0:
            self.__history_index -= 1
            self.__step_to_history_state(self.__history[self.__history_index])
            self.print_attribute_table()
        self.__update_undo_redo()

    def __redo(self) -> None:
        """Move forward one step in the history."""
        if self.__history_index < len(self.__history) - 1:
            self.__history_index += 1
            self.__step_to_history_state(self.__history[self.__history_index])
            self.print_attribute_table()
        self.__update_undo_redo()

    def __update_undo_redo(self) -> None:
        """Set the undo and redo buttons as enabled or disabled appropriately."""
        self.undo_button.setEnabled(self.__history_index > 0)
        self.redo_button.setEnabled(self.__history_index < len(self.__history) - 1)

    def __step_to_history_state(self, state: list[list[str]] | QCheckBox) -> None:
        """Change the state of the table and data to match the given state.

        :param state: The state to step into
        """
        if isinstance(state, QCheckBox):
            state.setChecked(state.isChecked)
        else:
            self.attributes_table.synonyms = copy.deepcopy(state)

    def add_state_to_history(self, state: list[list[str]] | QCheckBox) -> None:
        """Add a state to the end of the history and deal with redunndant entries if appropriate.

        :param state: The state to add
        """
        if self.__history_index < len(self.__history) - 1:
            self.__history = copy.deepcopy(self.__history[0 : self.__history_index + 1])
            self.__history_index = self.__history_index + 1
        if self.__history_index < len(self.__history):
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

    def print_attribute_table(self) -> None:
        """Print Attribute Table"""
        self.attributes_table.clearContents()
        self.attributes_table.setColumnCount(len(self.__attributes_list))
        self.attributes_table.setHorizontalHeaderLabels(self.__attributes_list)

        max_row_count: int = 0
        for j, attrbutes in enumerate(self.__attributes_list):
            unique_attributes: list[tuple[str, int]] = self.__calculate_distribution(
                self.__participants_list, attrbutes
            )

            if max_row_count < len(unique_attributes):
                max_row_count = len(unique_attributes)
                self.attributes_table.setRowCount(max_row_count)

            for i, (attr, nmb) in enumerate(unique_attributes):
                self.attributes_table.set_value(i, j, attr, nmb)

            if len(self.__checkboxes) <= j:
                checkbox: QCheckBox = QCheckBox()
                checkbox.setParent(self.centralWidget())
                checkbox.setText("")
                reference_item: QTableWidgetItem = self.attributes_table.item(0, j)
                reference_index: QModelIndex = self.attributes_table.indexFromItem(
                    reference_item
                )
                ref: QRect = self.attributes_table.visualRect(reference_index)
                checkbox.setGeometry(
                    QRect(ref.left() + int(0.5 * ref.width() + 15), 130, 30, 30)
                )
                checkbox.setVisible(True)
                checkbox.setChecked(False)
                if attrbutes.lower() not in [
                    "name",
                    "first name",
                    "last name",
                    "vorname",
                    "nachname",
                    "angemeldet",
                    "status",
                    "title",
                    "titel",
                ]:
                    checkbox.setChecked(True)
                self.__checkboxes.append(checkbox)
            self.attributes_table.repaint()

    def __filter_enabled_attributes(self) -> list[str]:
        enabled_attributes: list[str] = []
        for i in range(len(self.__attributes_list)):
            if self.__checkboxes[i].isChecked():
                enabled_attributes.append(list(self.__attributes_list)[i])
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
            for entry in result:
                old_entry = entry
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
        return result


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow
    if len(sys.argv) < 2:
        window = MainWindow("assets/main_window.ui")
    else:
        window = MainWindow(*sys.argv[1:])
    window.show()

    app.exec()
