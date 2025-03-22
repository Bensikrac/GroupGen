from PyQt6.QtCore import QObject, pyqtSignal
from data_structures import Participant, Assignment
from algorithm.simulated_annealing_algorithm import SimulatedAnnealingAlgorithm


class AlgorithmWorker(QObject):
    """Algorithm worker thread object."""

    finished = pyqtSignal(object)
    progress = pyqtSignal(int, int)

    algorithm_instance: SimulatedAnnealingAlgorithm
    participants: set[Participant]
    number_of_groups: int
    number_of_iterations: int
    number_of_epochs: int

    def run(self) -> None:
        """Run the algorithm"""
        self.finished.emit(
            self.algorithm_instance.find_assignment(
                self.participants,
                self.number_of_groups,
                self.number_of_iterations,
                self.number_of_epochs,
                progress_callback=self.progress.emit,
            )
        )
