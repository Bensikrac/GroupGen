from math import comb, factorial
from data_structures import Participant


class ObjectiveFunction:
    """Contains all calculations necessary to evaluate the quality of a group assignment"""

    @staticmethod
    def calculate_mix_cost(self, rounds: list[list[set[Participant]]]) -> float:
        """Calculates a score between 0 and 1 based on the number of different participants each participant meets, the lower the better"""
        cost: float = 0
        participant_count: int = 0
        groups: list[set[Participant]] = []
        for round in rounds:
            for group in round:
                groups += group

        for group in rounds[0]:
            participant_count += len(group)

        groups2: list[set[Participant]] = list(groups)
        for group in groups:
            groups2.remove(group)
            for group2 in groups2:
                cost += len(group.intersection(group2))

        max_cost: float = comb(len(rounds), 2) * participant_count

        return cost / max_cost
