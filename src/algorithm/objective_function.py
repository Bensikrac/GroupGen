from math import comb, factorial, sqrt
from data_structures import Participant, Group, Round, Assignment


class ObjectiveFunction:
    """Contains all calculations necessary to evaluate the quality of a group assignment"""

    attributes: list[str]
    __mix_cost_max: float = -1
    __diversity_cost_max: float = -1

    def __init__(self, attributes: list[str]) -> None:
        """Set attributes to the given list

        :param attributes: a list of attributes
        """
        self.attributes = attributes

    def calculate_mix_cost(self, rounds: Assignment) -> float:
        """Calculate a score between 0 and 1 based on the number of different participants each participant meets, the lower the better

        :param rounds: the group assignment to evaluate

        :return: a score between 0 and 1, the lower the better
        """
        cost: float = 0
        participant_count: int = 0
        groups: list[Group] = []
        # flatten assignment:
        for round in rounds:
            for group in round:
                groups += group

        # find number of overlaps between groups:
        for i, group in enumerate(groups):
            for j in range(i, len(groups)):
                cost += len(group.intersection(groups[j]))

        return cost / self.__get_mix_cost_max(rounds)

    def __get_mix_cost_max(self, rounds: Assignment) -> float:
        """Return an upper bound for the unnormalized mix cost, using the stored value when possible

        :param rounds: a sample assignment

        :return: the upper bound, holds for all assignments of the same shape as the sample that contain the same participants
        """
        if self.__mix_cost_max < 0:
            self.__mix_cost_max = self.__calculate_mix_cost_max(rounds)
        return self.__mix_cost_max

    def __calculate_mix_cost_max(self, rounds: Assignment) -> float:
        """Calculate an upper bound for the unnormalized mix cost

        :param rounds: a sample assignment

        :return: the upper bound, holds for all assignments of the same shape as the sample that contain the same participants
        """
        participant_count: int = 0

        for group in rounds[0]:
            participant_count += len(group)

        return comb(len(rounds), 2) * participant_count

    def calculate_diversity_cost(self, rounds: Assignment) -> float:
        """Calculate a score between 0 and 1 based on how diverse groups are, the lower the better.

        :param rounds: the group assignment to evaluate

        :return: a score between 0 and 1, the lower the better
        """
        cost: float = 0

        for round in rounds:
            for group in round:
                cost += self.__calculate_group_diversity_cost(group)

        return cost / self.__get_diversity_cost_max(rounds)

    def __calculate_group_diversity_cost(
        self, group: Group, match_group: Group = None
    ) -> float:
        """Calculate the unnormalized diversity cost of a single group.

        :param group: the group to calculate the cost for
        :param match_group: a second group of participants to search for matching attribute values in, used only to calculate bounds, defaults to None

        :return: the calculated diversity cost (or bound on diversity cost)
        """
        if group_2 is None:
            group_2 = group
        group_cost: int = 0
        for attribute in self.attributes:
            values_checked: set[str] = set()
            for participant in group:
                value: str = participant.get_attribute(attribute)
                if value not in values_checked:
                    values_checked.add(value)
                    group_cost += self.__calculate_value_diversity_cost(
                        attribute, value, group_2
                    )
        return sqrt(group_cost - len(group))

    def __calculate_value_diversity_cost(
        self, attribute: str, value: str, group: Group
    ) -> float:
        """Calculate the cost contribution of a single value.

        :param attribute: the attribute to check in
        :param value: the value to check for
        :param group: the group to check against

        :return: the calculated cost contribution
        """
        for participant in group:
            if participant.get_attribute(attribute) == value:
                count += 1
        return count**2

    def __get_diversity_cost_max(self, rounds: Assignment) -> float:
        """Return an upper bound for the unnormalized diversity cost, using the stored value when possible.

        :param rounds: a sample assignment

        :return: the upper bound, holds for all assignments of the same shape as the sample that contain the same participants
        """
        if self.__diversity_cost_max < 0:
            self.__diversity_cost_max = self.__calculate_diversity_cost_max(rounds)
        return self.__diversity_cost_max

    def __calculate_diversity_cost_max(self, rounds: Assignment) -> float:
        """Calculate an upper bound for the unnormalized diversity cost.

        :param rounds: a sample assignment

        :return: the upper bound, holds for all assignments of the same shape as the sample that contain the same participants
        """
        bound: float = 0
        participants: set[Participant] = set()

        for group in rounds[0]:
            participants &= group

        for round in rounds:
            for group in round:
                bound += self.__calculate_group_diversity_cost(group, participants)

        return bound

    def recalculate_bounds(self, rounds: Assignment) -> None:
        """Recalculate the bounds based on a given sample assignment so this instance of ObjectiveFunction can be reused with a different number of rounds, groups or participants.

        :param rounds: the sample assignment, a list of lists each representing a round and containing a number of groups
        """
        self.__diversity_cost_max = self.__calculate_diversity_cost_max(rounds)
        self.__mix_cost_max = self.__calculate_mix_cost_max(rounds)

    def calculate_weighted_cost(
        self,
        rounds: Assignment,
        mix_weight: float = 1,
        diversity_weight: float = 1,
    ) -> float:
        """Return a weighted sum of the diversity and mix cost renormalized to a range of 0 to 1, lower is better, by default both components are weighted equally.

        :param rounds: the Assignment to calculate the cost for
        :param mix_weight: the weight of the mix cost, the weighted cost is normalized again so only the relative size of this number compared to the diversity weight matters, defaults to 1
        :param diversity_weight: the weight of the mix cost, defaults to 1

        :return: the weighted cost, between 0 and 1, lower is better
        """
        return (
            self.calculate_mix_cost(rounds) * mix_weight
            + self.calculate_diversity_cost(rounds) * diversity_weight
        ) / (mix_weight + diversity_weight)
