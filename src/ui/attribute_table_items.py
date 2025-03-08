"""Module containing cells for the attribute table"""

from enum import Enum
from typing import override
from PyQt6.QtWidgets import QTableWidgetItem


class MergeableAttributeItem(QTableWidgetItem):
    """A QTableWidgetItem that stores its value while displaying the value with a count.

    :param value: The value for the item
    :param count: The count for the item
    """

    value: str

    def __init__(self, value: str, count: int) -> None:
        super().__init__(f"{count}: {value}")
        self.value = value


class AttributeState(Enum):
    """The state of an attribute/column of the attribute table.
    """
    NORMAL = 0
    DEACTIVATED = 1
    PRIORITIZED = 2
    DEPRIORITIZED = 3


class CheckableHeaderItem(QTableWidgetItem):
    """A QTablewidgetItem that stores a state.

    :param text: The text the item is labeled with, defaults to ""
    :param state: The state the item starts with, defaults to NORMAL
    """

    state: AttributeState

    def __init__(
        self, text: str = "", state: AttributeState = AttributeState.NORMAL
    ) -> None:
        super().__init__(text)
        self.state = state
