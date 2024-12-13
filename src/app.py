"""Main app to be launched"""

import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from excel_tool import Reader, Writer
from data_structures import Participant, Assignment
from algorithm.simulated_annealing_algorithm import SimulatedAnnealingAlgorithm


class MainWindow(QMainWindow):
    """Main Window class"""

    __input_path: os.PathLike | None = None
    __output_path: os.PathLike | None = None

    def __init__(self, ui_file_path: os.PathLike, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        uic.loadUi(ui_file_path, self)

        self.setWindowTitle("GroupGen")

        self.input_pick_button.clicked.connect(self.__input_file_picker)
        self.output_pick_button.clicked.connect(self.__output_file_picker)
        self.run_workflow_button.clicked.connect(self.__run_workflow)

    def __run_workflow(self) -> None:
        if self.__input_path is None:
            raise ValueError("Input Path not set")
        if self.__output_path is None:
            raise ValueError("Output Path not set")

        self.state_label.setText("Status: Preparing...")

        participant_list: list[Participant]
        algorithm_instance: SimulatedAnnealingAlgorithm
        final_assignment: Assignment

        excel_reader: Reader = Reader(self.__input_path)
        self.participant_list = excel_reader.read()

        p_set = set(self.participant_list)

        self.algorithm_instance = SimulatedAnnealingAlgorithm(
            list(self.participant_list[0].attributes.keys())
        )

        self.state_label.setText("Status: Calculating...")

        self.final_assignment = self.algorithm_instance.find_assignment(
            p_set,
            int(self.groups_spinbox.value()),
            int(self.iterations_spinbox.value()),
            50,
        )

        excel_writer: Writer = Writer(self.__output_path)
        excel_writer.write_file(self.final_assignment)

        self.state_label.setText("Status: Finished!")

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
