"""Main app to be launched"""

import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QCheckBox,
    QWidget,
)
from PyQt6.QtCore import Qt, QRect, QModelIndex
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

    def __init__(self, ui_file_path: os.PathLike, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        uic.loadUi(ui_file_path, self)

        self.attributes_table.set_main_window(self)

        self.setWindowTitle("GroupGen")

        self.input_pick_button.clicked.connect(self.__input_file_picker)
        self.read_input_button.clicked.connect(self.__read_input_file)
        self.output_pick_button.clicked.connect(self.__output_file_picker)
        self.run_algorithm_button.clicked.connect(self.__run_workflow)
        # self.select_synonym_button.clicked.connect()

        self.read_input_button.setEnabled(False)
        self.run_algorithm_button.setEnabled(False)
        # self.select_synonym_button.setEnabled(False)
        self.select_synonym_label.setVisible(False)

    def __run_workflow(self) -> None:
        """Executes the algorithm and and writes the output."""
        if self.__input_path is None:
            raise ValueError("Input Path not set")
        if self.__output_path is None:
            raise ValueError("Output Path not set")

        self.state_label.setText("Status: Preparing...")

        algorithm_instance: SimulatedAnnealingAlgorithm = SimulatedAnnealingAlgorithm(
            self.__filter_enabled_attributes()
        )
        self.__synonym_filter_participants()

        self.state_label.setText("Status: Calculating...")

        final_assignment: Assignment = algorithm_instance.find_assignment(
            set(self.__participants_list),
            int(self.groups_spinbox.value()),
            int(self.iterations_spinbox.value()),
            1000,
        )

        Writer(self.__output_path).write_file(final_assignment)

        self.state_label.setText("Status: Finished!")

    def __synonym_filter_participants(self):
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

        self.read_input_button.setEnabled(True)

    def __read_input_file(self) -> None:
        """Read Input File Button Function"""

        self.state_label.setText("Status: Reading...")
        self.__set_buttons_enabled(False)

        self.__participants_list = Reader(self.__input_path).read()
        self.__attributes_list = self.__participants_list[0].attributes.keys()

        # Print Table
        self.attributes_table.synonyms = []
        self.print_attribute_table()

        self.state_label.setText("Status: Finished Reading...")
        self.select_synonym_label.setVisible(True)
        self.__set_buttons_enabled(True)

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
        self.attributes_table.setColumnCount(len(self.__attributes_list))
        self.attributes_table.setHorizontalHeaderLabels(self.__attributes_list)

        max_row_count: int = 0
        for j, attrbutes in enumerate(self.__attributes_list):
            unique_attributes: list[(str, int)] = self.__calculate_distribution(
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
                # checkbox.destroyed.connect(
                #    lambda: print(f"{checkbox.text()} destroyed")
                # )
                checkbox.setText("")
                # ref: QRect = self.attributes_table.visualItemRect(
                #    self.attributes_table.horizontalHeaderItem(j)
                # )
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
        self.read_input_button.setEnabled(enable)
        self.output_pick_button.setEnabled(enable)
        self.run_algorithm_button.setEnabled(enable)
        # self.select_synonym_button.setEnabled(enable)

    def __calculate_distribution(
        self, participants: list[Participant], attribute: str
    ) -> list[(str, int)]:
        """Returns a list of values for the given attribute and how often each value appears.

        :param: participants: The list of participants to search in
        :param: attribute: The attribute to find values for

        :return: A list of tuples, each containing a value and how many times it appears.
        """
        result: list[(str, int)] = []
        for participant in participants:
            temp_value: str = participant.get_attribute(attribute)
            if not temp_value:
                continue
            temp_bool: bool = False
            old_temp_value: tuple[str, int]
            new_temp_value: tuple[str, int]
            for entry in result:
                old_temp_value = entry
                if old_temp_value[0] == self.attributes_table.find_preferred_synonym(
                    temp_value
                ):
                    new_temp_value = (old_temp_value[0], old_temp_value[1] + 1)
                    temp_bool = True
                    break
            if not temp_bool:
                result.append(
                    (self.attributes_table.find_preferred_synonym(temp_value), 1)
                )
            else:
                result.remove(old_temp_value)
                result.append(new_temp_value)
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
