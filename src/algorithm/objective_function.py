from math import comb, factorial, sqrt
from data_structures import Participant


class ObjectiveFunction:
    """Contains all calculations necessary to evaluate the quality of a group assignment"""

    attributes: list[str]
    __mix_cost_max: float = -1
    __diversity_cost_max: float = -1

    def __init__(self, attributes: list[str]) -> None:
        self.attributes = attributes

    def __init__(
        self, attributes: list[str], rounds: list[list[set[Participant]]]
    ) -> None:
        self.attributes = attributes
        self.recalculate_bounds(rounds)

    def calculate_mix_cost(self, rounds: list[list[set[Participant]]]) -> float:
        """Calculates a score between 0 and 1 based on the number of different participants each participant meets, the lower the better"""
        cost: float = 0
        participant_count: int = 0
        groups: list[set[Participant]] = []
        for round in rounds:
            for group in round:
                groups += group

        groups2: list[set[Participant]] = list(groups)
        for group in groups:
            groups2.remove(group)
            for group2 in groups2:
                cost += len(group.intersection(group2))

        return cost / self.__calculate_mix_cost_max(rounds)

    def __get_mix_cost_max(self, rounds: list[list[set[Participant]]]) -> float:
        """Returns an upper bound for the unnormalized mix cost, using the stored value when possible"""
        if self.__get_mix_cost_max < 0:
            self.__mix_cost_max = self.__calculate_mix_cost_max(rounds)

    def __calculate_mix_cost_max(self, rounds: list[list[set[Participant]]]) -> float:
        """Calculates an upper bound for the unnormalized mix cost"""
        participant_count: int = 0

        for group in rounds[0]:
            participant_count += len(group)

        return comb(len(rounds), 2) * participant_count

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

        return cost / self.__calculate_diversity_cost_max(rounds)

    def __get_diversity_cost_max(self, rounds: list[list[set[Participant]]]) -> float:
        """Returns an upper bound for the unnormalized diversity cost, using the stored value when possible"""
        if self.__get_diversity_cost_max < 0:
            self.__diversity_cost_max = self.__calculate_diversity_cost_max(rounds)

    def __calculate_diversity_cost_max(
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

    def recalculate_bounds(self, rounds: list[list[set[Participant]]]) -> None:
        self.__diversity_cost_max = self.__calculate_diversity_cost_max(rounds)
        self.__mix_cost_max = self.__calculate_mix_cost_max(rounds)

    def calculate_weighted_cost(
        self,
        rounds: list[list[set[Participant]]],
        mix_weight: float = 1,
        diversity_weight: float = 1,
    ) -> float:
        """Returns a weighted sum of the diversity and mix cost renormalized to a range of 0 to 1, lower is better, by default both components are weighted equally"""
        return (
            self.calculate_mix_cost(rounds) * mix_weight
            + self.calculate_diversity_cost(rounds) * diversity_weight
        ) / (mix_weight + diversity_weight)
