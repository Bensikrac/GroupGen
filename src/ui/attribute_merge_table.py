"""Module containing the classes for the attribute frequency table."""

import copy
from typing import override
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHeaderView
from PyQt6.QtGui import (
    QMouseEvent,
    QDrag,
    QDropEvent,
    QDragEnterEvent,
    QDragMoveEvent,
    QFont,
)
from PyQt6.QtCore import Qt, QMimeData
from app import MainWindow
from ui.attribute_table_items import CheckableHeaderItem, MergeableAttributeItem


class AttributeMergeTable(QTableWidget):
    """A QtableWidtet to display attribute value frequencies that can be merged via drag and drop."""

    frequencies: list[tuple[str, int]] = []
    synonyms: list[list[str]] = []
    values: list[list[str]] = []
    dragged_item: MergeableAttributeItem | None
    __main_window: MainWindow

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        header = self.horizontalHeader()
        header.sectionClicked.connect(self.__header_click)

    def __header_click(self, col: int):
        clicked_item = self.horizontalHeaderItem(col)
        if isinstance(clicked_item, CheckableHeaderItem):
            clicked_item.checked = not clicked_item.checked
            font: QFont = QFont()
            # font.setBold(clicked_item.checked)
            font.setStrikeOut(not clicked_item.checked)
            clicked_item.setFont(font)
            self.update()

    def set_main_window(self, main_window: MainWindow) -> None:
        """Sets the table's connected main window to a given value.

        :param main_window: The main window to set as this table's main window
        """
        self.__main_window = main_window

    @override
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Starts a drag and saves the original dragged item.

        :param event: The triggering event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            clicked_item = self.itemAt(event.pos())

            if isinstance(clicked_item, MergeableAttributeItem):
                self.dragged_item = clicked_item

                drag: QDrag = QDrag(self)
                mime_data: QMimeData = QMimeData()
                drag.setMimeData(mime_data)
                drag.exec()

    @override
    def dropEvent(self, event: QDropEvent) -> None:
        """Accepts the drop if it is valid cell and updates the synonyms and table accordingly

        :param event: The triggering event
        """
        target_cell: QTableWidgetItem = self.itemAt(event.position().toPoint())
        if (
            target_cell is not None
            and isinstance(target_cell, MergeableAttributeItem)
            and target_cell.value != self.dragged_item.value
            and self.column(target_cell) == self.column(self.dragged_item)
        ):
            # self.main_window.add_state_to_history(copy.deepcopy(self.synonyms))

            target_list: list[str]
            for synonym_list in self.synonyms:
                if (
                    target_cell.value == synonym_list[0]
                    and not self.dragged_item.value in synonym_list
                ):
                    target_list = synonym_list
                    break
            else:
                target_list = [target_cell.value]
                self.synonyms.append(target_list)
            old_list: list[str] = self.find_synonyms_for_value(self.dragged_item.value)
            target_list.extend(old_list)
            if old_list in self.synonyms:
                self.synonyms.remove(old_list)
            self.__main_window.construct_attribute_table()
            event.accept()
            self.__main_window.add_state_to_history(copy.deepcopy(self.synonyms))
        self.dragged_item = None

    def find_synonyms_for_value(self, value: str) -> list[str]:
        """Returns the list of values that the given value is the preferred synonym for.

        :param value: The value to find the list of synonyms for
        :return: The list of corresponding synonyms
        """
        for synonym_list in self.synonyms:
            if value == synonym_list[0]:
                return synonym_list
        return [value]

    def find_preferred_synonym(self, value: str) -> str:
        """Returns the preferred synonym for the given value.

        :param value: The given value
        :return: The preferred synonym (the original value if no more preferred synonym exists)
        """
        for synonym_list in self.synonyms:
            if value in synonym_list:
                return synonym_list[0]
        return value

    @override
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        event.accept()

    @override
    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        event.accept()

    def set_value(self, row: int, column: int, value: str, count: int) -> None:
        """Sets the item at a given row and column to a MergeableAttributeItem with given parameters

        :param row: The row to set the item in
        :param column: The column to set the item in
        :param value: The value for the MergeableAttributeItem
        :param count: The count for the MergeableAttributeItem
        """
        self.setItem(row, column, MergeableAttributeItem(value, count))
        self.values = []
