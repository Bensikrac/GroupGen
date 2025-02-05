"""Simulated Annealing algorithm module"""

from copy import copy
from math import exp
from random import Random
from typing import Any, Callable
from algorithm.objective_function import ObjectiveFunction
from algorithm.random_algorithm import RandomAlgorithm
from data_structures import Assignment, Iteration, Participant


class SimulatedAnnealingAlgorithm:
    """Contains the calculations for generating group assignments using simulated annealing.

    :param attributes: A list of attributes that are considered for optimization
    :param random_instance: An instance of Random that will be used
    instead of an automatically generated one as a source or randomness, defaults to None
    """

    __random: Random
    attributes: list[str]

    temperatures: list[float] = []
    scores: list[float] = []

    def __init__(self, attributes: list[str], random_instance: Random = None):
        self.__random = Random() if random_instance is None else random_instance
        self.attributes = attributes

    def find_assignment(
        self,
        participants: set[Participant],
        groups_per_iteration: int,
        iterations: int,
        max_cycles: int,
        intitial_temperature: float = 1,
        temperature_scaling: float = 15,
        mix_weight: float = 1,
        diversity_weight: float = 1,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> Assignment:
        """Return a group assignment generated using simulated annealing.

        :param participants: the set of participants to distribute into groups
        :param groups_per_iteration: the number of groups in each iteration
        :param iterations: the total number of iterations
        :param max_cycles: the maximum number of times
        the algorithm will iteratively improve the assignment
        :param intitial_temperature: the initial Temperature, deafults to 1
        :param temperature_scaling: controls the rate of temperature decay, higher means quicker,
        defaults to 15
        :param mix_weight: the weight of the mix cost when evaluating assignments,
        only the size of this number compared to the diversity weight matters, defaults to 1
        :param diversity_weight: the weight of the diversity cost, defaults to 1
        :param progress_callback: gets called with current progress and total progress (optional)

        :return: the generated assignment
        """
        random: RandomAlgorithm = RandomAlgorithm(self.__random)
        assignment: Assignment = random.find_assignment(
            participants, groups_per_iteration, iterations
        )
        objective: ObjectiveFunction = ObjectiveFunction(self.attributes)
        if progress_callback is not None:
            progress_callback(0, max_cycles)
        for i in range(1, max_cycles + 1):
            temperature: float = self.get_temperature(
                i / max_cycles, intitial_temperature, temperature_scaling
            )
            neighbor: Assignment = self.find_neighbor(assignment)
            if self.__should_take_step(
                assignment,
                neighbor,
                temperature,
                objective,
                mix_weight,
                diversity_weight,
            ):
                assignment = neighbor
            self.scores.append(
                objective.calculate_weighted_cost(
                    assignment, mix_weight, diversity_weight
                )
            )
            if progress_callback is not None:
                progress_callback(i, max_cycles)
        return assignment

    def __should_take_step(
        self,
        assignment: Assignment,
        neighbor: Assignment,
        temperature: float,
        objective: ObjectiveFunction,
        mix_weight: float,
        diversity_weight: float,
    ) -> bool:
        """Determines whether the algorithm takes the step to a given neighbor.

        :param assignment: the current assignment
        :param neighbor: the neighboring assignment
        :param temperature: the current temperature
        :param objective: the objective function to use
        :param mix_weight: the weight of the mix cost when evaluating assignments,
        only the size of this number compared to the diversity weight matters
        :param diversity_weight: the weight of the diversity cost

        :return: true if the steep should be taken, false otherwise
        """
        return (
            self.get_step_probability(
                objective.calculate_weighted_cost(
                    assignment, mix_weight, diversity_weight
                ),
                objective.calculate_weighted_cost(
                    neighbor, mix_weight, diversity_weight
                ),
                temperature,
            )
            >= self.__random.random()
        )

    def get_temperature(
        self, progress: float, intitial_temperature: float, scaling: float
    ) -> float:
        """Calculate the temperature for a given progress through the annealing process.

        :param progress: The fraction of the maximum cycles for the process that has passed
        :param intitial_temperature: The initial temperature
        :param scaling: Controls the rate of exponential decay, higher means quicker decay

        :return: The temperature value
        """

        temperature: float = (
            intitial_temperature * (1 - progress) * exp(-scaling * progress)
        )

        self.temperatures.append(temperature)

        return temperature

    def find_neighbor(self, assignment: Assignment) -> Assignment:
        """Return a random group assignment that is one swap removed from the given assignment.

        :param assignment: The assignment to find a neighbor for

        :return: The found neighbor
        """
        neighbor: Assignment = self.__half_deep_copy(assignment)
        index = self.__random.randrange(len(assignment))
        iteration: Iteration = assignment[index]
        group_index_1: int = self.__random.randrange(len(iteration))
        participant_index_1: int = self.__random.randrange(
            len(iteration[group_index_1])
        )

        group_index_2: int = -1
        while group_index_2 in (-1, group_index_1):
            group_index_2 = self.__random.randrange(len(iteration))
        participant_index_2: int = self.__random.randrange(
            len(iteration[group_index_2])
        )

        self.__swap_between_sets(
            neighbor[index][group_index_1],
            neighbor[index][group_index_2],
            list(iteration[group_index_1])[participant_index_1],
            list(iteration[group_index_2])[participant_index_2],
        )
        return neighbor

    def __swap_between_sets(
        self, set_1: set, set_2: set, element_1: Any, element_2: Any
    ) -> None:
        """Swaps two elements between two sets.

        :param set_1: the first set
        :param set_2: the second set
        :param element_1: the first element, initially in set_1
        :param element_2: the second element, initially in set_2
        """
        set_1.discard(element_1)
        set_2.add(element_1)
        set_2.discard(element_2)
        set_1.add(element_2)

    def __half_deep_copy(self, obj: Any) -> Any:
        """Return a recursive deep copy of the given object
        that stops at any element that isn't a set or list.

        :param obj: The object to copy

        :return: The copy
        """
        if isinstance(obj, list):
            return [self.__half_deep_copy(item) for item in obj]
        if isinstance(obj, set):
            return {self.__half_deep_copy(item) for item in obj}
        return copy(obj)

    def get_step_probability(
        self, energy_old: float, energy_new: float, temperature: float
    ) -> float:
        """Return the probability of taking a step from an assignment to another.

        :param energy_old: The cost of the old assignment
        :param energy_new: The cost of the new assignment
        :param temperature: The current temperature

        :return: The probability of taking the step, based on the Metropolis criterion
        """
        if energy_new < energy_old:
            return 1
        if temperature <= 0:
            return 0
        return exp(-(energy_new - energy_old) / temperature)
