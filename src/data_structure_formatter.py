"""Module providing formatting functions for data structures."""

from data_structures import Participant, Group, Iteration, Assignment, ListOfRowLists


def append_rows(x: ListOfRowLists[str], y: ListOfRowLists[str]) -> ListOfRowLists[str]:
    """Combine 2 2-dimensional lists by the outer lists.

    Outer-list-wise appending :param:`y` to :param:`x`

    :param x: List
    :param y: List

    :return: Combined list
    """
    return x + y


def append_columns(
    x: ListOfRowLists[str], y: ListOfRowLists[str]
) -> ListOfRowLists[str]:
    """Combine 2 2-dimensional lists by their inner lists.

    Inner-list-wise appending :param:`y` to :param:`x`

    :param x: List
    :param y: List

    :return: Combined list
    """
    # make x and y same sized
    if len(x) < len(y):
        x += [[str()]] * (len(y) - len(x))
    elif len(y) < len(x):
        y += [[str()]] * (len(x) - len(y))

    retval: ListOfRowLists[str] = []
    for a, b in zip(x, y):
        retval.append(a + b)
    return retval


def empty_row(n: int) -> ListOfRowLists[str]:
    """Create a string matrix with an empty row of size :param:`n`.

    :param n: Size of the row

    :return: String matrix with one row of size :param:`n`
    """
    return [[str()] * n]


def empty_column(n: int) -> ListOfRowLists[str]:
    """Create a string matrix with an empty column of size :param:`n`.

    :param n: Size of the column

    :return: String matrix with :param:`n` rows of size 1
    """
    return list([[str()]] * n)


def participant_to_str_matrix(
    participant: Participant,
    attributes_to_print: list[str] | None = None,
    delimiter: str | None = None,
) -> ListOfRowLists[str]:
    """Convert a :class:`Participant` to a string matrix.

    :param participant: :class:`Participant` to convert
    :param attributes_to_print: Optionally only print attribute values for these attribute classes
    (uses :func:`__str__` of :class:`Participant` when `None`)
    :param delimiter: Optional delimiter between each attribute to print, defaults to `'_'`

    :return: String matrix of converted :class:`Participant`
    """
    if delimiter is None:
        delimiter = "_"
    return (
        [
            [
                delimiter.join(
                    [
                        value
                        for key, value in participant.attributes.items()
                        if key in attributes_to_print
                    ]  # get attribute values of selected classes
                )  # put `delimiter` in-between
            ]  # wrap in double list for format
        ]
        if attributes_to_print is not None
        else [[str(participant)]]  # just use string representation
    )


def group_to_str_matrix(
    group: Group,
    attributes_to_print: list[str] | None = None,
    delimiter: str | None = None,
) -> ListOfRowLists[str]:
    """Convert a :class:`Group` to a string matrix.

    :param group: :class:`Group` to convert
    :param attributes_to_print: Optionally only print these attribute classes
    (forwarded to :func:`participant_to_str_matrix`)
    :param delimiter: Optional delimiter between each attribute to print, defaults to `'_'`
    (forwarded to :func:`participant_to_str_matrix`)

    :return: String matrix of converted :class:`Group`
    """
    retval: ListOfRowLists[str] = []
    for participant in group:
        retval = append_rows(
            retval,
            participant_to_str_matrix(participant, attributes_to_print, delimiter),
        )
    return retval


def iteration_to_str_matrix(
    iteration: Iteration,
    attributes_to_print: list[str] | None = None,
    delimiter: str | None = None,
) -> ListOfRowLists[str]:
    """Convert a :class:`Iteration` to a string matrix.

    :param iteration: :class:`Iteration` to convert
    :param attributes_to_print: Optionally only print these attribute classes
    (forwarded to :func:`participant_to_str_matrix`)
    :param delimiter: Optional delimiter between each attribute to print, defaults to `'_'`
    (forwarded to :func:`participant_to_str_matrix`)

    :return: String matrix of converted :class:`Iteration`
    """
    retval: ListOfRowLists[str] = []
    for i, group in enumerate(iteration):
        if i == 0:
            retval = group_to_str_matrix(group, attributes_to_print, delimiter)
        else:
            retval = append_columns(retval, empty_column(len(group)))
            retval = append_columns(
                retval, group_to_str_matrix(group, attributes_to_print, delimiter)
            )
    return retval


def assignment_to_str_matrix(
    assignment: Assignment,
    attributes_to_print: list[str] | None = None,
    delimiter: str | None = None,
) -> ListOfRowLists[str]:
    """Convert a :class:`Assignment` to a string matrix.

    :param assignment: :class:`Assignment` to convert
    :param attributes_to_print: Optionally only print these attribute classes
    (forwarded to :func:`participant_to_str_matrix`)
    :param delimiter: Optional delimiter between each attribute to print, defaults to `'_'`
    (forwarded to :func:`participant_to_str_matrix`)

    :return: String matrix of converted :class:`Assignment`
    """
    retval: ListOfRowLists[str] = [["Assignment"]]
    for i, iteration in enumerate(assignment):
        if i != 0:
            retval = append_rows(retval, empty_row(len(retval[-1])))
        retval = append_rows(retval, [[f"Iteration {i+1}"]])
        retval = append_rows(
            retval, iteration_to_str_matrix(iteration, attributes_to_print, delimiter)
        )
    return retval


def str_matrix_to_participant_set(m: ListOfRowLists[str]) -> set[Participant]:
    """Convert a list of rows of str to a set of :class:`Participant`s.

    :param m: String matrix to convert.

    :return: Set of :class:`Participant`s
    """
    retval = set()

    for i in range(1, len(m)):
        if len(m[0]) != len(m[i]):
            raise ValueError(
                f"Attribute classes and values not equal length for Participant {i}"
            )
        retval.add(Participant(i, dict(zip(m[0], m[i]))))
