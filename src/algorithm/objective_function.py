"""Module containing the objective function."""

from math import comb, sqrt
from data_structures import Participant, Group, Assignment


class ObjectiveFunction:
    """Contains all calculations necessary to evaluate the quality of a group assignment"""

    __attribute_classes: list[str]
    __cached_mix_cost_max: float
    __cached_diversity_cost_max: float

    def __init__(self, attribute_classes: list[str]) -> None:
        """Set attributes to the given list

        :param attributes: a list of attributes
        """
        self.__attribute_classes = attribute_classes
        self.__cached_mix_cost_max = -1.0
        self.__cached_diversity_cost_max = -1.0

    def mix_cost(self, assignment: Assignment) -> float:
        """Calculate a score based on the number of different participants each participant meets

        :param assignment: the group assignment to evaluate

        :return: a score between 0 and 1, the lower the better
        """
        cost: float = 0.0
        groups: list[Group] = [
            group for iteration in assignment for group in iteration
        ]  # list of all groups in assignment

        for i, group in enumerate(groups):
            for j in range(i + 1, len(groups)):
                cost += max(len(group.intersection(groups[j])) - 1, 0)

        return cost / self.__mix_cost_max(assignment)

    def __mix_cost_max(self, sample_assignment: Assignment) -> float:
        """Return an upper bound for the unnormalized mix cost,
          using the stored value when possible

        :param sample_assignment: a sample assignment

        :return: the upper bound,
          holds for all assignments of the same shape
        """
        if self.__cached_mix_cost_max < 0.0:
            participant_count: int = 0
            for group in sample_assignment[0]:
                participant_count += len(group)
            self.__cached_mix_cost_max = (
                comb(len(sample_assignment), 2) * participant_count
            )
        return self.__cached_mix_cost_max

    def diversity_cost(self, assignment: Assignment) -> float:
        """Calculate a score between 0 and 1 based on how diverse groups are, the lower the better.

        :param assignment: the group assignment to evaluate

        :return: a score between 0 and 1, the lower the better
        """
        return self.__total_group_diversity_cost(
            assignment
        ) / self.__diversity_cost_max(assignment)

    def __total_group_diversity_cost(
        self, assignment: Assignment, match_group: Group | None = None
    ) -> float:
        """Calculate the summed unnormalized diversity cost of all groups in an assignment.

        :param assignment: the assignment
        :param match_group: a group of participants to search for matching attribute values in,
        used only to calculate bounds, defaults to None
        :return: the sum of the unnormalized diversity costs of all groups in the assignment
        """
        cost: float = 0.0
        for iteration in assignment:
            for group in iteration:
                cost += self.__group_diversity_cost(group, match_group)
        return cost

    def __group_diversity_cost(
        self, group: Group, match_group: Group | None = None
    ) -> float:
        """Calculate the unnormalized diversity cost of a single group.

        :param group: the group to calculate the cost for
        :param match_group: a second group of participants to search for matching attribute values,
        used only to calculate bounds, defaults to None

        :return: the calculated diversity cost (or bound on diversity cost)
        """
        group_cost: float = 0.0
        for attribute in self.__attribute_classes:
            values_checked: set[str] = set()
            for participant in group:
                value: str = participant.get_attribute(attribute)
                if value not in values_checked:
                    values_checked.add(value)
                    group_cost += self.__value_diversity_cost(
                        attribute, value, group if match_group is None else match_group
                    )
        return sqrt(group_cost - len(group))

    def __value_diversity_cost(self, attribute: str, value: str, group: Group) -> float:
        """Calculate the cost contribution of a single value.

        :param attribute: the attribute to check in
        :param value: the value to check for
        :param group: the group to check against

        :return: the calculated cost contribution
        """

        count: float = 0.0

        for participant in group:
            if participant.get_attribute(attribute) == value:
                count += 1.0
        return count**2

    def __diversity_cost_max(self, sample_assignment: Assignment) -> float:
        """Return an upper bound for the unnormalized diversity cost,
        using the stored value when possible.

        :param sample_assignment: a sample assignment

        :return: the upper bound,
        holds for all assignments of the same shape that contain the same participants
        """
        participants: set[Participant] = set()
        for group in sample_assignment[0]:
            participants = participants.union(group)

        if self.__cached_diversity_cost_max < 0.0:
            self.__cached_diversity_cost_max = self.__total_group_diversity_cost(
                sample_assignment, participants
            )

        return self.__cached_diversity_cost_max

    def recalculate_bounds(self, sample_assignment: Assignment) -> None:
        """Recalculate the bounds based on a given sample assignment

        :param sample_assignment: the sample assignment,
        a list of lists each representing a round and containing a number of groups
        """
        self.__cached_diversity_cost_max = -1.0
        self.__diversity_cost_max(sample_assignment)

        self.__cached_mix_cost_max = -1.0
        self.__mix_cost_max(sample_assignment)

    def calculate_weighted_cost(
        self,
        assignment: Assignment,
        mix_weight: float = 1.0,
        diversity_weight: float = 1.0,
    ) -> float:
        """Return a weighted sum of the diversity and mix cost renormalized to a range of 0 to 1,
        lower is better, by default both components are weighted equally.

        :param assignment: the Assignment to calculate the cost for
        :param mix_weight: the weight of the mix cost,
        only the size of this number compared to the diversity weight matters, defaults to 1
        :param diversity_weight: the weight of the diversity cost, defaults to 1

        :return: the weighted cost, between 0 and 1, lower is better
        """
        return (
            self.mix_cost(assignment) * mix_weight
            + self.diversity_cost(assignment) * diversity_weight
        ) / (mix_weight + diversity_weight)
