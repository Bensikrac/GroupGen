from copy import copy
from math import exp
from random import Random
from typing import Any
from algorithm.objective_function import ObjectiveFunction
from algorithm.random_algorithm import RandomAlgorithm
from data_structures import Group, Participant


class SimulatedAnnealingAlgorithm:
    """Calculates group assignments using simulated annealing"""

    __random: Random
    attributes: list[str]

    def __init__(self, attributes: list[str] = []):
        self.__random = Random()
        self.attributes = attributes

    def __init__(self, random: Random, attributes: list[str] = []):
        self.__random = random
        self.attributes = attributes

    def find_assignment(
        self,
        participants: set[Participant],
        groups_per_round: int,
        rounds: int,
        max_iterations: int,
    ) -> list[list[Group]]:
        """Returns a group assignment generated using simulated annealing"""
        random: RandomAlgorithm = RandomAlgorithm(self.__random)
        assignment: list[list[Group]] = random.find_assignment(
            participants, groups_per_round, rounds
        )
        objective: ObjectiveFunction = ObjectiveFunction(self.attributes, assignment)
        for i in range(max_iterations):
            temperature: int = self.get_temperature(1 - (i + 1) / max_iterations)
            neighbor: list[list[Group]] = self.find_neighbor(assignment)
            if (
                self.get_step_probability(
                    objective.calculate_mix_cost(assignment),
                    objective.calculate_mix_cost(neighbor),
                    temperature,
                )
                >= self.__random.random()
            ):
                assignment = neighbor
        return assignment

    def get_temperature(self, progress: float) -> float:
        """Calculates the temperature for a given progress through the annealing process"""
        return 100 * 0.1 ** (progress) - 10

    def find_neighbor(self, assignment: list[list[Group]]) -> list[list[Group]]:
        """Returns a random group assignment that is one swap removed from the given assignment"""
        neighbor = self.__half_deep_copy(assignment)
        round: int = self.__random.randrange(len(assignment))
        group_index_1: int = self.__random.randrange(len(assignment[round]))
        participant_index_1: int = self.__random.randrange(
            len(assignment[round][group_index_1].get_members)
        )

        group_index_2: int = -1
        participant_index_2: int = -1
        while (group_index_2 is -1) or (group_index_1 is group_index_2):
            group_index_2 = self.__random.randrange(len(assignment[round]))
            participant_index_2 = self.__random.randrange(
                len(assignment[round][group_index_2].get_members)
            )

        participant_1: Participant = assignment[round][group_index_1].get_members()[
            participant_index_1
        ]
        participant_2: Participant = assignment[round][group_index_2].get_members()[
            participant_index_2
        ]
        assignment[round][group_index_1].remove_participant(participant_1)
        assignment[round][group_index_1].add_participant(participant_2)
        assignment[round][group_index_2].remove_participant(participant_2)
        assignment[round][group_index_2].add_participant(participant_1)

        return assignment

    def __half_deep_copy(self, object: Any) -> Any:
        """Returns a recursive deep copy of the given object that stops at any element that isn't a Group, set or list"""
        if isinstance(object, list) or isinstance(object, set):
            return [self.__half_deep_copy(item) for item in object]
        elif isinstance(object, Group):
            return Group([self.__half_deep_copy(item) for item in object.get_members()])
        else:
            return copy(object)

    def get_step_probability(
        self, energy_old: float, energy_new: float, temperature: float
    ) -> float:
        """Returns the probability between 0 and 1 of taking a step from an assignment with the givven old energy to one with the given new energy"""
        if energy_new < energy_old:
            return 1
        else:
            return exp(-(energy_new - energy_old) / temperature)
