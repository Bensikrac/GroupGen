"""Module containing tests for the simulated annealing algorithm."""

from random import Random
from data_structures import Assignment, Participant
from algorithm.simulated_annealing_algorithm import SimulatedAnnealingAlgorithm
from algorithm.random_algorithm import RandomAlgorithm
from algorithm.objective_function import ObjectiveFunction


def test_find_assignment():
    """Tests whether find_assignment generates assignments of the correct shape."""
    participants: list[Participant] = [
        Participant(0, {"gender": "m", "nationalität": "mordor", "fb": "1"}),
        Participant(1, {"gender": "m", "nationalität": "gondor", "fb": "2"}),
        Participant(2, {"gender": "m", "nationalität": "gondor", "fb": "3"}),
        Participant(3, {"gender": "w", "nationalität": "gondor", "fb": "3"}),
        Participant(4, {"gender": "w", "nationalität": "lindon", "fb": "2"}),
        Participant(5, {"gender": "w", "nationalität": "mordor", "fb": "1"}),
        Participant(6, {"gender": "m", "nationalität": "angmar", "fb": "2"}),
        Participant(7, {"gender": "m", "nationalität": "angmar", "fb": "2"}),
        Participant(8, {"gender": "w", "nationalität": "angmar", "fb": "3"}),
        Participant(9, {"gender": "d", "nationalität": "mordor", "fb": "1"}),
        Participant(10, {"gender": "d", "nationalität": "mordor", "fb": "1"}),
    ]
    test_seed_1: int = 11112222
    test_algorithm: SimulatedAnnealingAlgorithm = SimulatedAnnealingAlgorithm(
        list(participants[0].attributes.keys()), Random(test_seed_1)
    )
    test_assignment_1: Assignment = test_algorithm.find_assignment(
        set(participants), 2, 3, 50
    )
    assert len(test_assignment_1[0][0]) == 6
    assert len(test_assignment_1[0][1]) == 5
    assert len(test_assignment_1[1][0]) == 6
    assert len(test_assignment_1[1][1]) == 5
    assert len(test_assignment_1[2][0]) == 6
    assert len(test_assignment_1[2][1]) == 5

    test_assignment_2: Assignment = test_algorithm.find_assignment(
        set(participants), 4, 2, 50
    )
    assert len(test_assignment_2[0][0]) == 3
    assert len(test_assignment_2[0][1]) == 3
    assert len(test_assignment_2[0][2]) == 3
    assert len(test_assignment_2[0][3]) == 2
    assert len(test_assignment_2[1][0]) == 3
    assert len(test_assignment_2[1][1]) == 3
    assert len(test_assignment_2[1][2]) == 3
    assert len(test_assignment_2[1][3]) == 2


def test_quality():
    """Tests whether simualted annealing with 100 iterations performs better than brute force with 500."""
    participants: list[Participant] = [
        Participant(0, {"gender": "m", "nationalität": "mordor", "fb": "1"}),
        Participant(1, {"gender": "m", "nationalität": "gondor", "fb": "2"}),
        Participant(2, {"gender": "m", "nationalität": "gondor", "fb": "3"}),
        Participant(3, {"gender": "w", "nationalität": "gondor", "fb": "3"}),
        Participant(4, {"gender": "w", "nationalität": "lindon", "fb": "2"}),
        Participant(5, {"gender": "w", "nationalität": "mordor", "fb": "1"}),
        Participant(6, {"gender": "m", "nationalität": "angmar", "fb": "2"}),
        Participant(7, {"gender": "m", "nationalität": "angmar", "fb": "2"}),
        Participant(8, {"gender": "w", "nationalität": "angmar", "fb": "3"}),
        Participant(9, {"gender": "d", "nationalität": "mordor", "fb": "1"}),
        Participant(10, {"gender": "d", "nationalität": "mordor", "fb": "1"}),
    ]
    test_seed_1: int = 11112222
    random_algorithm: RandomAlgorithm = RandomAlgorithm(Random(test_seed_1))
    annealing_algorithm: SimulatedAnnealingAlgorithm = SimulatedAnnealingAlgorithm(
        list(participants[0].attributes.keys()), Random(test_seed_1)
    )
    annealing_assignment: Assignment = annealing_algorithm.find_assignment(
        set(participants), 4, 3, 100
    )
    brute_force_assignment: Assignment = random_algorithm.brute_force_assignment(
        set(participants), 4, 3, 500
    )

    objective: ObjectiveFunction = ObjectiveFunction(participants[0].attributes.keys())
    assert objective.calculate_weighted_cost(
        annealing_assignment
    ) < objective.calculate_weighted_cost(brute_force_assignment)
