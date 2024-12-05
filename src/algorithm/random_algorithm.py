"""Random algorithm module"""

from copy import copy
from math import ceil
from random import Random
import random
from data_structures import Assignment, Group, Participant


class RandomAlgorithm:
    """Calculates group assignments using randomness

    :param random: An instance of Random that will be used
    instead of an automatically generated one as a source or randomness, defaults to None
    """

    __random: Random

    def __init__(self, random: Random = None):
        if random is None:
            self.__random = Random()
        else:
            self.__random = random

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
        assignment: Assignment = list()
        for i in range(iterations):
            remaining_participants: set[Participant] = copy(participants)
            round: list[Group] = list()
            for j in range(groups_per_iteration):
                group: Group = set()
                for k in range(max_group_size):
                    if len(remaining_participants) is 0:
                        break
                    participant: Participant = self.__random.choice(
                        tuple(remaining_participants)
                    )
                    group.add(participant)
                    remaining_participants.discard(participant)
                round.append(group)
            assignment.append(round)

        return assignment
