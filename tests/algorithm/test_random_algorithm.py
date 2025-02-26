"""Module containing tests for the random algorithm."""

from random import Random
from algorithm.random_algorithm import RandomAlgorithm
from algorithm.objective_function import ObjectiveFunction
from data_structures import Assignment, Participant


def test_random_seed():
    """Tests whether the algorithm is correctly initialized with a given Random."""
    test_seed_1: int = 11112222
    test_seed_2: int = 2025
    test_algorithm_1: RandomAlgorithm = RandomAlgorithm(Random(test_seed_1))
    test_algorithm_2: RandomAlgorithm = RandomAlgorithm(Random(test_seed_2))
    assert (
        test_algorithm_1._RandomAlgorithm__random.random()
        == Random(test_seed_1).random()
    )
    assert (
        test_algorithm_2._RandomAlgorithm__random.random()
        == Random(test_seed_2).random()
    )


def test_find_assignment():
    """Tests whether find_assignment generates assignments of the correct shape"""
    test_seed_1: int = 11112222
    test_algorithm: RandomAlgorithm = RandomAlgorithm(Random(test_seed_1))
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
    test_assignment_1: Assignment = test_algorithm.find_assignment(
        set(participants), 2, 3
    )
    assert len(test_assignment_1[0][0]) == 6
    assert len(test_assignment_1[0][1]) == 5
    assert len(test_assignment_1[1][0]) == 6
    assert len(test_assignment_1[1][1]) == 5
    assert len(test_assignment_1[2][0]) == 6
    assert len(test_assignment_1[2][1]) == 5

    test_assignment_2: Assignment = test_algorithm.find_assignment(
        set(participants), 4, 2
    )
    assert len(test_assignment_2[0][0]) == 3
    assert len(test_assignment_2[0][1]) == 3
    assert len(test_assignment_2[0][2]) == 3
    assert len(test_assignment_2[0][3]) == 2
    assert len(test_assignment_2[1][0]) == 3
    assert len(test_assignment_2[1][1]) == 3
    assert len(test_assignment_2[1][2]) == 3
    assert len(test_assignment_2[1][3]) == 2


def test_brute_force():
    """Tests whether brute force with 200 iterations performs better than a single random"""
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
    test_algorithm: RandomAlgorithm = RandomAlgorithm(Random(test_seed_1))
    random_assignment: Assignment = test_algorithm.find_assignment(
        set(participants), 4, 3
    )
    brute_force_assignment: Assignment = test_algorithm.brute_force_assignment(
        set(participants), 4, 3, 200
    )

    objective: ObjectiveFunction = ObjectiveFunction(participants[0].attributes.keys())
    assert objective.calculate_weighted_cost(
        brute_force_assignment
    ) < objective.calculate_weighted_cost(random_assignment)
