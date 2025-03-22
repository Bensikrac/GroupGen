"""Main app to be launched"""

import copy
from operator import itemgetter
import os
from random import Random
import sys
import time
import ctypes
from typing import override

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QMessageBox,
    QPushButton,
    QAbstractButton,
)
from PyQt6.QtGui import QDesktopServices, QIcon, QGuiApplication, QFocusEvent
from PyQt6.QtCore import QUrl, Qt, QProcess, QDir
from algorithm.objective_function import ObjectiveFunction
from algorithm.simulated_annealing_algorithm import SimulatedAnnealingAlgorithm
from ui.attribute_table_items import AttributeState, CheckableHeaderItem
from excel_tool import Reader, Writer
from data_structures import Participant, Assignment
from assets.main_window import Ui_MainWindow

type HistoryState = list[list[str]]


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window class

    Takes args and kwargs like :class:`QMainWindow`.
    """

    # pylint: disable=too-few-public-methods

    __input_path: os.PathLike | None = None
    __output_path: os.PathLike | None = None
    __participants_list: list[Participant]
    __attributes_list: list[str]
    __history: list[HistoryState] = [[]]
    __history_index: int = 0

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.attributes_table.set_main_window(self)

        self.setWindowTitle("GroupGen")
        # self.setWindowIcon(QIcon(asset_path("groupgen_logo3_icon.ico")))
        QApplication.setWindowIcon(QIcon(asset_path("groupgen_logo3_icon.ico")))

        if sys.platform.startswith("win32"):
            app_id = "impulse.groupgen.app"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        self.input_pick_button.clicked.connect(self.__input_file_picker)
        # self.read_input_button.clicked.connect(self.__read_input_file)
        self.output_pick_button.clicked.connect(self.__output_file_picker)
        self.run_algorithm_button.clicked.connect(self.__run_algorithm)
        # self.select_synonym_button.clicked.connect()
        self.reset_synonyms_button.clicked.connect(self.__reset_synonyms)
        self.undo_button.clicked.connect(self.__undo)
        self.redo_button.clicked.connect(self.__redo)
        self.sorting_comboBox.currentIndexChanged.connect(
            self.construct_attribute_table
        )

        # self.read_input_button.setEnabled(False)
        self.run_algorithm_button.setEnabled(False)
        # self.select_synonym_button.setEnabled(False)
        self.select_synonym_label.setVisible(False)
        self.weigh_attribute_label.setVisible(False)
        self.undo_button.setEnabled(False)
        self.redo_button.setEnabled(False)
        self.reset_synonyms_button.setEnabled(False)
        self.sorting_comboBox.setEnabled(False)

        ignored_text: str = (
            "<span style='color: rgba(0, 0, 0, 150);'><s>ignored,</s></span>"
        )
        if QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            ignored_text = (
                "<span style='color: rgba(255, 255, 255, 150);'><s>ignored,</s></span>"
            )

        self.weigh_attribute_label.setTextFormat(Qt.TextFormat.RichText)
        self.weigh_attribute_label.setText(
            "Click on a column header to switch between that attribute being treated normally, "
            + ignored_text
            + "<span style='color: rgb(20, 200, 50);'><b> prioritized by a factor of 2</b></span>"
            + " or "
            + "<span style='color: rgb(225, 50, 50);'><i>deprioritized by a factor 2</i></span>"
            + " by the algorithm"
        )

        output_progress_size_policy = self.output_progress.sizePolicy()
        output_progress_size_policy.setRetainSizeWhenHidden(True)
        self.output_progress.setSizePolicy(output_progress_size_policy)
        self.output_progress.setVisible(False)

    def __run_algorithm(self) -> None:
        """Executes the algorithm and and writes the output."""
        if self.__input_path is None:
            raise ValueError("Input Path not set")
        if self.__output_path is None:
            raise ValueError("Output Path not set")

        self.state_label.setText("Status: Preparing...")
        self.state_label.repaint()

        start_time: float = time.time()

        filtered_attributes: list[str] = self.__filter_enabled_attributes()
        algorithm_instance: SimulatedAnnealingAlgorithm = SimulatedAnnealingAlgorithm(
            filtered_attributes, Random(), self.__get_attribute_weights()
        )

        self.state_label.setText("Status: Calculating...")
        self.state_label.repaint()

        self.output_progress.setValue(0)
        self.output_progress.setVisible(True)

        final_assignment: Assignment = algorithm_instance.find_assignment(
            self.__synonym_filter_participants(),
            int(self.groups_spinbox.value()),
            int(self.iterations_spinbox.value()),
            1000,
            progress_callback=self.__progress_callback,
        )

        Writer(self.__output_path).write_file(final_assignment)

        self.state_label.setText("Status: Finished!")
        self.state_label.repaint()

        time_passed: float = time.time() - start_time
        objective: ObjectiveFunction = ObjectiveFunction(filtered_attributes)
        average_participants_met: float = objective.average_meetings(final_assignment)
        mix_cost: float = objective.mix_cost(final_assignment)
        diversity_cost: float = objective.diversity_cost(final_assignment)
        weighted_cost: float = objective.calculate_weighted_cost(final_assignment)

        message_box: QMessageBox = QMessageBox()
        message_box.setTextFormat(Qt.TextFormat.RichText)
        message_box.setText(
            f"Algorithm executed successfully in {round(time_passed, 1)} seconds"
        )
        message_box.setInformativeText(
            f"Group assignments saved to {self.__output_path}"
        )
        message_box.setDetailedText(
            f"The average participant encounters {round(average_participants_met, 1)} distinct other participants in this assignment."
            + os.linesep
            + os.linesep
            + f"(weighted cost: {round(weighted_cost, 4)},  mix cost: {round(mix_cost, 4)}, diversity cost: {round(diversity_cost, 4)})"
        )
        # message_box.setStandardButtons(
        #    QMessageBox.StandardButton.Open | QMessageBox.StandardButton.Ok
        # )

        ok_button: QPushButton | None = message_box.addButton(
            "Ok", QMessageBox.ButtonRole.AcceptRole
        )
        open_button: QPushButton | None = message_box.addButton(
            "Open File", QMessageBox.ButtonRole.ActionRole
        )
        explorer_button: QPushButton | None = None
        if sys.platform.startswith("win32"):
            explorer_button = message_box.addButton(
                "Show in Explorer", QMessageBox.ButtonRole.ActionRole
            )
        message_box.setDefaultButton(ok_button)
        message_box.setEscapeButton(ok_button)
        # message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setWindowTitle("GroupGen: Algorithm executed successfully!")
        message_box.exec()
        response: QAbstractButton | None = message_box.clickedButton()

        if response == open_button:
            QDesktopServices.openUrl(QUrl(self.__output_path))
        if response is not None and response == explorer_button:
            self.__open_in_explorer(self.__output_path)

    def __open_in_explorer(self, path: os.PathLike) -> None:
        """Opens the file explorer with the file at the given path highlighted if on windows.

        :param path: the path to the file to highlight
        """
        path = os.path.abspath(path)
        if sys.platform == "win32":
            args = []
            args.append("/select,")
            args.append(QDir.toNativeSeparators(path))
            QProcess.startDetached("explorer", args)

    def __progress_callback(self, current: int, maximum: int) -> None:
        """Callback for the progress bar

        :param current: current progress
        :param maximum: maximum progress
        """
        self.output_progress.setValue(int((float(current) / float(maximum)) * 100.0))
        self.output_progress.repaint()

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
            filtered_participants.add(Participant(attributes))
        return filtered_participants

    def __input_file_picker(self) -> None:
        """Select Input File Button Function"""
        if self.__input_path:
            preselected_dir = self.__input_path
        elif self.__output_path:
            preselected_dir = self.__output_path
        else:
            preselected_dir = "/"

        selected_path = QFileDialog.getOpenFileName(
            caption="select input file",
            directory=preselected_dir,
            filter="Excel Files (*.xlsx *.xls)",
        )[0]
        if selected_path:
            self.__input_path = selected_path

            self.output_progress.setVisible(False)
            self.input_file_path_line_edit.setText(self.__input_path)
            self.input_file_path_line_edit.repaint()

            # self.read_input_button.setEnabled(True)
            self.__read_input_file()

    def __read_input_file(self) -> None:
        """Read Input File Button Function"""

        self.state_label.setText("Status: Reading...")
        self.state_label.repaint()
        self.__set_buttons_enabled(False)

        self.__participants_list = Reader.read(self.__input_path)
        self.__attributes_list = self.__participants_list[0].attributes.keys()

        # Construct Table
        self.attributes_table.synonyms = []
        self.construct_attribute_table()

        self.state_label.setText("Status: Finished Reading...")
        self.state_label.repaint()
        self.select_synonym_label.setVisible(True)
        self.weigh_attribute_label.setVisible(True)
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
            self.__step_to_history_state(self.__history_index - 1)

    def __redo(self) -> None:
        """Move forward one step in the history."""
        if self.__history_index < len(self.__history) - 1:
            self.__step_to_history_state(self.__history_index + 1)

    def __update_undo_redo(self) -> None:
        """Set the undo and redo buttons as enabled or disabled appropriately."""
        self.undo_button.setEnabled(self.__history_index > 0)
        self.redo_button.setEnabled(self.__history_index < len(self.__history) - 1)

    def __step_to_history_state(self, state_index: int) -> None:
        """Change the state of the table and data to match the given state.

        :param state: The state to step into
        """
        state = self.__history[state_index]
        self.__history_index = state_index
        if isinstance(state, list):
            self.attributes_table.synonyms = copy.deepcopy(state)
        self.construct_attribute_table()
        self.__update_undo_redo()

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
        if self.__output_path:
            preselected_dir = self.__output_path
        elif self.__input_path:
            preselected_dir = self.__input_path
        else:
            preselected_dir = "/"

        selected_path = QFileDialog.getSaveFileName(
            caption="select output file",
            directory=preselected_dir,
            filter="Excel Files (*.xlsx *.xls)",
        )[0]

        if selected_path:
            if not (selected_path.endswith(".xlsx") or selected_path.endswith(".xls")):
                selected_path += ".xlsx"

            self.output_progress.setVisible(False)
            self.__output_path = selected_path
            self.output_file_path_line_edit.setText(self.__output_path)
            self.output_file_path_line_edit.repaint()

            self.run_algorithm_button.setEnabled(True)

    def construct_attribute_table(self) -> None:
        """Construct Attribute Table"""
        self.attributes_table.clearContents()
        self.attributes_table.setColumnCount(len(self.__attributes_list))
        # self.attributes_table.setHorizontalHeaderLabels(self.__attributes_list)

        max_row_count: int = 0
        for j, attrbutes in enumerate(self.__attributes_list):
            header_item: QTableWidgetItem | None = (
                self.attributes_table.horizontalHeaderItem(j)
            )
            if not (
                isinstance(header_item, CheckableHeaderItem)
                and header_item.text() == attrbutes
            ):
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
                    CheckableHeaderItem(
                        attrbutes,
                        (
                            AttributeState.NORMAL
                            if should_be_checked
                            else AttributeState.DEACTIVATED
                        ),
                    ),
                )

            unique_attributes: list[tuple[str, int]] = self.__calculate_distribution(
                self.__participants_list, attrbutes
            )

            if max_row_count < len(unique_attributes):
                max_row_count = len(unique_attributes)
                self.attributes_table.setRowCount(max_row_count)

            for i, (attr, nmb) in enumerate(unique_attributes):
                self.attributes_table.set_value(i, j, attr, nmb)

            new_header_item: CheckableHeaderItem = (
                self.attributes_table.horizontalHeaderItem(j)
            )
            self.attributes_table.update_column_visuals(j, new_header_item.state)

        self.attributes_table.update()

    def __filter_enabled_attributes(self) -> list[str]:
        enabled_attributes: list[str] = []
        for i in range(len(self.__attributes_list)):
            item: QTableWidgetItem = self.attributes_table.horizontalHeaderItem(i)
            if (
                isinstance(item, CheckableHeaderItem)
                and item.state != AttributeState.DEACTIVATED
            ):
                enabled_attributes.append(list(self.__attributes_list)[i])
        return enabled_attributes

    def __get_attribute_weights(self) -> dict[str, float]:
        attribute_weights: dict[str, float] = dict()
        for i in range(len(self.__attributes_list)):
            item: QTableWidgetItem = self.attributes_table.horizontalHeaderItem(i)
            if isinstance(item, CheckableHeaderItem):
                if item.state == AttributeState.PRIORITIZED:
                    attribute_weights[item.text()] = 2
                if item.state == AttributeState.DEPRIORITIZED:
                    attribute_weights[item.text()] = 0.5
        return attribute_weights

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
        self.sorting_comboBox.setEnabled(enable)

    def __sort_distribution(
        self, distribution: list[tuple[str, int]]
    ) -> list[tuple[str, int]]:
        """Function for sorting an attribute distribution. Returns the list sorted by Value (Ascending) if sorting
        is set to Names or sorted by 1. Frequency (Descending), 2. Value (Ascending) if sorting is set to Frequency

        :param distribution: current unsorted attribute distribution list

        :return: sorted attribute distribution list
        """

        if self.sorting_comboBox.currentText() == "Value":
            return sorted(distribution, key=itemgetter(0))
        return sorted(distribution, key=lambda x: (1 / x[1], x[0]))

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

        result = self.__sort_distribution(result)

        return result

    @override
    def focusOutEvent(self, event: QFocusEvent):
        """Reconstructs the table on focus-in to avoid weirdness with selection highlighting."""
        super().focusOutEvent(event)
        self.construct_attribute_table()


def main():
    """Entrypoint"""
    QApplication.setStyle("fusion")
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    app.exec()


def asset_path(relative_path) -> str:
    """Returns the path to an asset for usage with Qt, works as dev and with pyinstaller.
    Assumes the asset is in assets/ and added as data on the top level in pyinstaller.

    :param relative_path: The path to the asset relative to assets/
    :return: The path to the asset, transformed so it is usable as an asset in Qt without further modification
    """
    # pylint: disable=locally-disabled, protected-access, broad-exception-caught, no-member
    if sys.platform.startswith("win32"):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = "assets/"
    else:
        base_path = "assets/"

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    main()
