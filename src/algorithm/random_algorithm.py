"""Random algorithm module"""

from copy import copy
from math import ceil
from random import Random
from data_structures import Assignment, Group, Participant
from objective_function import ObjectiveFunction


class RandomAlgorithm:
    """Calculates group assignments using randomness

    :param random_instance: An instance of Random that will be used
    instead of an automatically generated one as a source or randomness, defaults to None
    """

    __random: Random

    def __init__(self, random_instance: Random = None):
        self.__random = Random() if random_instance is None else random_instance

    def find_assignment(
        self, participants: set[Participant], groups_per_iteration: int, iterations: int
    ) -> Assignment:
        """Return a randomly generated group assignment.

        :param participants: The set of participants to distribute into groups
        :param groups_per_round: The number of goups per iteration
        :param iterations: The number of iterations to generate groups for

        :return: The generated assignment
        """
        max_group_size: int = ceil(len(participants) / groups_per_iteration)
        assignment: Assignment = []
        for i in range(iterations):
            remaining_participants: set[Participant] = copy(participants)
            iteration: list[Group] = [set() for _ in range(groups_per_iteration)]
            for j in range(max_group_size):
                for group in iteration:
                    if len(remaining_participants) == 0:
                        break
                    participant: Participant = self.__random.choice(
                        tuple(remaining_participants)
                    )
                    group.add(participant)
                    remaining_participants.discard(participant)
            assignment.append(iteration)

        return assignment

    def brute_force_assignment(
        self,
        participants: set[Participant],
        groups_per_iteration: int,
        iterations: int,
        max_cycles: int,
    ) -> Assignment:
        """Generates a number of random assignments and returns the best.

        :param participants: The set of participants to distribute into groups
        :param groups_per_round: The number of goups per iteration
        :param iterations: The number of iterations to generate groups for
        :param max_cycles: The number of assignments to generate

        :return: The best assignment
        """
        best: Assignment = self.find_assignment(
            participants, groups_per_iteration, iterations
        )

        attributes: set[str] = list(participants)[0].attributes.keys()
        objective: ObjectiveFunction = ObjectiveFunction(list(attributes))

        best_score: float = objective.calculate_weighted_cost(best)

        for i in range(max_cycles):
            new: Assignment = self.find_assignment(
                participants, groups_per_iteration, iterations
            )
            new_score: float = objective.calculate_weighted_cost(new)
            if new_score < best_score:
                best = new
                best_score = new_score
        return best
