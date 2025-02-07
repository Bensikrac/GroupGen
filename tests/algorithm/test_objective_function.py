import pytest

from algorithm.objective_function import ObjectiveFunction
from data_structures import Assignment, Iteration, Group, Participant


@pytest.fixture
def participants() -> list[Participant]:
    participants: list[Participant] = [
        Participant(0, {"gender": "m", "nationalität": "mordor", "fb": "1"}),
        Participant(1, {"gender": "m", "nationalität": "gondor", "fb": "2"}),
        Participant(2, {"gender": "m", "nationalität": "gondor", "fb": "3"}),
        Participant(3, {"gender": "w", "nationalität": "gondor", "fb": "3"}),
        Participant(4, {"gender": "w", "nationalität": "lindon", "fb": "2"}),
        Participant(5, {"gender": "w", "nationalität": "mordor", "fb": "1"}),
    ]
    return participants


def test_average_meetings(participants):
    test_function: ObjectiveFunction = ObjectiveFunction(
        ["gender", "nationalität", "fb"]
    )
    group_men: Group = {participants[0], participants[1], participants[2]}
    group_women: Group = {participants[3], participants[4], participants[5]}
    group_gondor: Group = {participants[1], participants[2], participants[3]}
    group_not_gondor: Group = {participants[0], participants[4], participants[5]}
    iteration_1: Iteration = [group_men, group_women]
    iteration_2: Iteration = [group_gondor, group_not_gondor]
    assignment_1: Assignment = [iteration_1, iteration_1]
    assignment_2: Assignment = [iteration_1, iteration_2]
    assignment_3: Assignment = [iteration_2, iteration_2]

    assert test_function.average_meetings(assignment_1) == pytest.approx(2)
    assert test_function.average_meetings(assignment_2) == pytest.approx(10 / 3)
    assert test_function.average_meetings(assignment_3) == pytest.approx(2)


def test_init_objective_function():
    test_function: ObjectiveFunction = ObjectiveFunction(["lorem", "ipsum", "dolor"])
    assert test_function._ObjectiveFunction__attribute_classes == [
        "lorem",
        "ipsum",
        "dolor",
    ]


def test_mix_cost(participants):
    test_function: ObjectiveFunction = ObjectiveFunction(
        ["gender", "nationalität", "fb"]
    )
    group_men: Group = {participants[0], participants[1], participants[2]}
    group_women: Group = {participants[3], participants[4], participants[5]}
    group_gondor: Group = {participants[1], participants[2], participants[3]}
    group_not_gondor: Group = {participants[0], participants[4], participants[5]}
    iteration_1: Iteration = [group_men, group_women]
    iteration_2: Iteration = [group_gondor, group_not_gondor]
    assignment_1: Assignment = [iteration_1, iteration_1]
    assignment_2: Assignment = [iteration_1, iteration_2]
    assignment_3: Assignment = [iteration_2, iteration_2]

    assert test_function.mix_cost(assignment_1) > test_function.mix_cost(assignment_2)
    assert test_function.mix_cost(assignment_1) == test_function.mix_cost(assignment_3)


def test_diversity_cost(participants):
    test_function: ObjectiveFunction = ObjectiveFunction(
        ["gender", "nationalität", "fb"]
    )
    group_men: Group = {participants[0], participants[1], participants[2]}
    group_women: Group = {participants[3], participants[4], participants[5]}
    group_gondor: Group = {participants[1], participants[2], participants[3]}
    group_not_gondor: Group = {participants[0], participants[4], participants[5]}
    group_div_1: Group = {participants[0], participants[1], participants[4]}
    group_div_2: Group = {participants[2], participants[3], participants[5]}
    iteration_1: Iteration = [group_men, group_women]
    iteration_2: Iteration = [group_gondor, group_not_gondor]
    iteration_3: Iteration = [group_div_1, group_div_2]
    assignment_1: Assignment = [iteration_1, iteration_2]
    assignment_2: Assignment = [iteration_3, iteration_3]
    assignment_3: Assignment = [iteration_1, iteration_3]
    assert test_function.diversity_cost(assignment_1) > test_function.diversity_cost(
        assignment_2
    )
    assert test_function.diversity_cost(assignment_1) > test_function.diversity_cost(
        assignment_3
    )
    assert test_function.diversity_cost(assignment_3) > test_function.diversity_cost(
        assignment_2
    )


# def test_recalculate_bounds():
