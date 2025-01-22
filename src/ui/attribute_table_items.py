from typing import override
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtGui import (
    QMouseEvent,
    QFont,
)


class MergeableAttributeItem(QTableWidgetItem):
    """A QTableWidgetItem that stores its value while displaying the value with a count.

    :param value: The value for the item
    :param count: The count for the item
    """

    value: str

    def __init__(self, value: str, count: int) -> None:
        super().__init__(f"{count}: {value}")
        self.value = value


class CheckableHeaderItem(QTableWidgetItem):
    """A QTablewidgetItem that can be checked and unchecked with a click."""

    checked: bool

    def __init__(self, text: str = "", checked: bool = False) -> None:
        super().__init__(text)
        self.checked = checked
