from copy import copy
from math import ceil
from random import Random
import random
from data_structures import Group, Participant


class RandomAlgorithm:
    """Calculates group assignments using randomness"""

    __random: Random

    def __init__(self):
        self.__random = Random()

    def __init__(self, random: Random):
        self.__random = random

    def find_assignment(
        self, participants: set[Participant], groups_per_round: int, rounds: int
    ) -> list[list[Group]]:
        """Returns a randomly generated group assignment"""
        max_group_size: int = ceil(len(participants) / groups_per_round)
        assignment: list[list[Group]] = list()
        for i in range(rounds):
            remaining_participants: set[Participant] = copy(participants)
            round: list[Group] = list()
            for j in range(groups_per_round):
                group: Group = Group()
                for k in range(max_group_size):
                    participant: Participant = self.__random.choice(
                        tuple(remaining_participants)
                    )
                    group.add_participant(participant)
                    remaining_participants.discard(participant)
                round.append(group)
            assignment.append(round)

        return assignment
