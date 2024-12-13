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
        participant_list: list[Participant]
        algorithm_instance: SimulatedAnnealingAlgorithm
        final_assignment: Assignment

        if self.__input_path is not None:
            excel_reader: Reader = Reader(self.__input_path)
        else:
            raise ValueError("Input Path not set")

        self.participant_list = excel_reader.read()

        p_set = set(self.participant_list)

        self.algorithm_instance = SimulatedAnnealingAlgorithm(
            list(self.participant_list[0].attributes.keys())
        )

        self.final_assignment = self.algorithm_instance.find_assignment(
            p_set,
            4,
            3,
            50,
        )
        if self.__output_path is not None:
            excel_reader: Reader = Reader(self.__output_path)
        else:
            raise ValueError("Output Path not set")

        excel_writer: Writer = Writer(self.__output_path)
        excel_writer.write_file(self.final_assignment)

    @staticmethod
    def __file_dialog() -> os.PathLike:
        return QFileDialog.getOpenFileName(
            caption="pick file", directory="/home", filter="Excel Files (*.xls *.xlsx)"
        )[0]

    def __input_file_picker(self) -> None:
        self.__input_path = self.__file_dialog()

    def __output_file_picker(self) -> None:
        self.__output_path = self.__file_dialog()


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow("assets/main_window.ui")
    window.show()

    app.exec()
