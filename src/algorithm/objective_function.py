from math import comb, factorial, sqrt
from data_structures import Participant


class ObjectiveFunction:
    """Contains all calculations necessary to evaluate the quality of a group assignment"""

    attributes: list[str]

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

    def calculate_diversity_cost(self, rounds: list[list[set[Participant]]]) -> float:
        """Calculates a score between 0 and 1 based on how diverse groups are, the lower the better"""
        cost: float = 0
        participant_count: int = 0

        for group in rounds[0]:
            participant_count += len(group)

        for round in rounds:
            for group in round:
                group_cost: int = 0
                for attribute in self.attributes:
                    values_checked: set[str] = set()
                    for participant in group:
                        value: str = participant.get_attribute(attribute)
                        if value not in values_checked:
                            count: int = 1
                            values_checked.add(value)
                            for participant2 in group:
                                if (
                                    participant2 != participant
                                    and participant2.get_attribute(attribute) == value
                                ):
                                    count += 1
                            group_cost += count**2
                cost += sqrt(group_cost - len(group))

        return cost / self.calculate_diversity_cost_bound(rounds)

    def calculate_diversity_cost_bound(
        self, rounds: list[list[set[Participant]]]
    ) -> float:
        """Calculates an upper bound for the unnormalized diversity cost"""
        bound: float = 0
        participant_count: int = 0
        participants: set[Participant] = set()

        for group in rounds[0]:
            participant_count += len(group)
            participants += group

        for round in rounds:
            for group in round:
                group_cost: int = 0
                for attribute in self.attributes:
                    values_checked: set[str] = set()
                    for participant in group:
                        value: str = participant.get_attribute(attribute)
                        if value not in values_checked:
                            count: int = 1
                            values_checked.add(value)
                            for participant2 in participants:
                                if (
                                    participant2 != participant
                                    and participant2.get_attribute(attribute) == value
                                ):
                                    count += 1
                            group_cost += count**2
                bound += sqrt(group_cost - len(group))

        return bound
