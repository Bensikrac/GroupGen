"""Main app to be launched"""

import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from excel_tool import Reader, Writer
from data_structures import Participant, Assignment
from algorithm.simulated_annealing_algorithm import SimulatedAnnealingAlgorithm


class MainWindow(QMainWindow):
    """Main Window class"""

    # pylint: disable=too-few-public-methods

    __input_path: os.PathLike | None = None
    __output_path: os.PathLike | None = None

    def __init__(self, ui_file_path: os.PathLike, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        uic.loadUi(ui_file_path, self)

        self.setWindowTitle("GroupGen")

        self.input_pick_button.clicked.connect(self.__input_file_picker)
        self.output_pick_button.clicked.connect(self.__output_file_picker)
        self.run_workflow_button.clicked.connect(self.__run_workflow)

        self.__set_status("Waiting...")

    def __set_status(self, status: str) -> None:
        self.state_label.setText(status)
        self.state_label.repaint()

    def __run_workflow(self) -> None:
        if self.__input_path is None:
            raise ValueError("Input Path not set")
        if self.__output_path is None:
            raise ValueError("Output Path not set")

        self.__set_status("Status: Reading file...")

        participant_list: list[Participant] = Reader(self.__input_path).read()
        participant_set: set[Participant] = set(participant_list)

        self.__set_status("Status: Calculating...")

        algorithm_instance: SimulatedAnnealingAlgorithm = SimulatedAnnealingAlgorithm(
            list(participant_list[0].attributes.keys())
        )

        final_assignment: Assignment = algorithm_instance.find_assignment(
            participant_set,
            int(self.groups_spinbox.value()),
            int(self.iterations_spinbox.value()),
            1000,
        )

        Writer(self.__output_path).write_file(final_assignment)

        self.__set_status("Status: Finished!")

    def __input_file_picker(self) -> None:
        self.__input_path = QFileDialog.getOpenFileName(
            caption="pick file", directory="/home", filter="Excel Files (*.xlsx *.xls)"
        )[0]
        self.input_file_path_line_edit.setText(self.__input_path)

    def __output_file_picker(self) -> None:
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


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow
    if len(sys.argv) < 2:
        window = MainWindow("assets/main_window.ui")
    else:
        window = MainWindow(*sys.argv[1:])
    window.show()

    app.exec()
