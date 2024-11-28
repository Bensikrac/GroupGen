from data_structures import Participant


class ObjectiveFunction:
    """Contains all calculations necessary to evaluate the quality of a group assignment"""

    @staticmethod
    def calculate_mix_cost(self, rounds: list[list[set[Participant]]]) -> float:
        """Calculates a cost based on the number of different participants each participant meets, the lower the better, the minimum score is 0"""
        score: float = 0
        groups: list[set[Participant]] = []
        for round in rounds:
            for group in round:
                groups += group

        for group in groups:
            for group2 in groups:
                if group != group2:
                    score += len(group.intersection(group2))

        return score
