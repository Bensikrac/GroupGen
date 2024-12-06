"""Module containing the objective function."""

from math import comb, sqrt
from dataset import Dataset
from data_structures import Group, Assignment


class ObjectiveFunction:
    """Contains all calculations necessary to evaluate the quality of a group assignment"""

    __dataset: Dataset
    __attributes: list[str]
    __cached_mix_cost_max: float = -1
    __cached_diversity_cost_max: float = -1

    def __init__(self, dataset: Dataset) -> None:
        """Set attributes to the given list

        :param attributes: a list of attributes
        """
        self.__dataset = dataset
        self.__attributes = dataset.attribute_classes

    def calculate_mix_cost(self, assignment: Assignment) -> float:
        """Calculate a score based on the number of different participants each participant meets

        :param assignment: the group assignment to evaluate

        :return: a score between 0 and 1, the lower the better
        """
        cost: float = 0
        groups: list[Group] = []
        # flatten assignment:
        for iteration in assignment:
            for group in iteration:
                groups += group

        for i, group in enumerate(groups):
            for j in range(i, len(groups)):
                cost += len(group.intersection(groups[j]))

        return cost / self.__mix_cost_max(assignment)

    def __mix_cost_max(self, sample_assignment: Assignment) -> float:
        """Return an upper bound for the unnormalized mix cost,
          using the stored value when possible

        :param sample_assignment: a sample assignment

        :return: the upper bound,
          holds for all assignments of the same shape
        """
        if self.__cached_mix_cost_max < 0:
            self.__cached_mix_cost_max = self.__calculate_mix_cost_max(
                sample_assignment
            )
        return self.__cached_mix_cost_max

    def __calculate_mix_cost_max(self, sample_assignment: Assignment) -> float:
        """Calculate an upper bound for the unnormalized mix cost

        :param sample_assignment: a sample assignment

        :return: the upper bound,
          holds for all assignments of the same shape
        """
        return comb(len(sample_assignment), 2) * self.__dataset.number_of_participants

    def calculate_diversity_cost(self, assignment: Assignment) -> float:
        """Calculate a score between 0 and 1 based on how diverse groups are, the lower the better.

        :param assignment: the group assignment to evaluate

        :return: a score between 0 and 1, the lower the better
        """
        return self.__calculate_total_group_diversity_cost(
            assignment
        ) / self.__diversity_cost_max(assignment)

    def __calculate_total_group_diversity_cost(
        self, assignment: Assignment, match_group=None
    ) -> float:
        """Calculate the summed unnormalized diversity cost of all groups in an assignment.

        :param assignment: the assignment
        :param match_group: a group of participants to search for matching attribute values in,
        used only to calculate bounds, defaults to None
        :return: the sum of the unnormalized diversity costs of all groups in the assignment
        """
        cost: float = 0
        for iteration in assignment:
            for group in iteration:
                cost += self.__calculate_group_diversity_cost(group, match_group)
        return cost

    def __calculate_group_diversity_cost(
        self, group: Group, match_group: Group = None
    ) -> float:
        """Calculate the unnormalized diversity cost of a single group.

        :param group: the group to calculate the cost for
        :param match_group: a second group of participants to search for matching attribute values,
        used only to calculate bounds, defaults to None

        :return: the calculated diversity cost (or bound on diversity cost)
        """
        if match_group is None:
            match_group = group
        group_cost: int = 0
        for attribute in self.__attributes:
            values_checked: set[str] = set()
            for participant in group:
                value: str = participant.get_attribute(attribute)
                if value not in values_checked:
                    values_checked.add(value)
                    group_cost += self.__calculate_value_diversity_cost(
                        attribute, value, match_group
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

    def __diversity_cost_max(self, sample_assignment: Assignment) -> float:
        """Return an upper bound for the unnormalized diversity cost,
        using the stored value when possible.

        :param sample_assignment: a sample assignment

        :return: the upper bound,
        holds for all assignments of the same shape that contain the same participants
        """
        if self.__cached_diversity_cost_max < 0:
            self.__cached_diversity_cost_max = self.__calculate_diversity_cost_max(
                sample_assignment
            )

        return self.__cached_diversity_cost_max

    def __calculate_diversity_cost_max(self, sample_assignment: Assignment) -> float:
        """Calculate an upper bound for the unnormalized diversity cost.

        :param sample_assignment: a sample assignment

        :return: the upper bound,
        holds for all assignments of the same shape that contain the same participants
        """
        return self.__calculate_total_group_diversity_cost(
            sample_assignment, self.__dataset.participants
        )

    def recalculate_bounds(self, sample_assignment: Assignment) -> None:
        """Recalculate the bounds based on a given sample assignment

        :param sample_assignment: the sample assignment,
        a list of lists each representing a round and containing a number of groups
        """
        self.__cached_diversity_cost_max = self.__calculate_diversity_cost_max(
            sample_assignment
        )
        self.__cached_mix_cost_max = self.__calculate_mix_cost_max(sample_assignment)

    def calculate_weighted_cost(
        self,
        assignment: Assignment,
        mix_weight: float = 1,
        diversity_weight: float = 1,
    ) -> float:
        """Return a weighted sum of the diversity and mix cost renormalized to a range of 0 to 1,
        lower is better, by default both components are weighted equally.

        :param assignment: the Assignment to calculate the cost for
        :param mix_weight: the weight of the mix cost,
        only the size of this number compared to the diversity weight matters, defaults to 1
        :param diversity_weight: the weight of the mix cost, defaults to 1

        :return: the weighted cost, between 0 and 1, lower is better
        """
        return (
            self.calculate_mix_cost(assignment) * mix_weight
            + self.calculate_diversity_cost(assignment) * diversity_weight
        ) / (mix_weight + diversity_weight)
