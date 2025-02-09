"""Module containing the classes for the attribute frequency table."""

import copy
from typing import override
from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)
from PyQt6.QtGui import QMouseEvent, QFont, QWheelEvent, QColor
from PyQt6.QtCore import Qt
from ui.attribute_table_items import CheckableHeaderItem, MergeableAttributeItem
from PyQt6.QtCore import QPoint, QModelIndex, QEvent


class AttributeMergeTable(QTableWidget):
    """A QtableWidtet to display attribute value frequencies that can be merged via drag and drop."""

    frequencies: list[tuple[str, int]] = []
    synonyms: list[list[str]] = []
    values: list[list[str]] = []
    __dragged_item: MergeableAttributeItem | None = None
    __main_window: "MainWindow"

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        header = self.horizontalHeader()
        header.sectionClicked.connect(self.__header_click)
        self.setStyleSheet(
            """
            QTableWidget::item:selected {
                background: transparent;
                color: black;
            }
        """
        )
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.verticalScrollBar().valueChanged.connect(lambda: self.clearSelection())
        self.horizontalScrollBar().valueChanged.connect(lambda: self.clearSelection())
        self.setMouseTracking(False)
        self.viewport().setMouseTracking(False)
        self.setStyleSheet("QTableWidget::item:hover { background: none; }")

    def __header_click(self, col: int) -> None:
        clicked_item = self.horizontalHeaderItem(col)
        if isinstance(clicked_item, CheckableHeaderItem):
            newcount: int = (
                int(self.__main_window.excluded_column_number_label.text()) + 1
                if clicked_item.checked
                else int(self.__main_window.excluded_column_number_label.text()) - 1
            )
            self.__main_window.excluded_column_number_label.setText(str(newcount))

            if clicked_item.checked == False:
                self.setColumnWidth(col, 100)
                for i in range(0, self.rowCount()):
                    if self.item(i, col) is not None:
                        self.item(i, col).setBackground(QColor("#FFFFFF"))
                        self.item(i, col).setForeground(QColor("#000000"))
            else:
                self.setColumnWidth(col, 1)
                for i in range(0, self.rowCount()):
                    if self.item(i, col) is not None:
                        self.item(i, col).setBackground(QColor("#AAAFB4"))
                        self.item(i, col).setForeground(QColor("#555555"))
            clicked_item.checked = not clicked_item.checked
            font: QFont = QFont()
            # font.setBold(clicked_item.checked)
            font.setStrikeOut(not clicked_item.checked)
            clicked_item.setFont(font)
            self.update()

    def set_main_window(self, main_window: "MainWindow") -> None:
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
                self.__dragged_item = clicked_item
        # else:
        # super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Accepts the drop if one is ongoing and updates synonyms and table accordingly.

        :param event: The triggering event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            target_cell: QTableWidgetItem = self.itemAt(event.position().toPoint())
            if self.__can_drop(event.position().toPoint()):
                target_list: list[str]
                for synonym_list in self.synonyms:
                    if (
                        target_cell.value == synonym_list[0]
                        and not self.__dragged_item.value in synonym_list
                    ):
                        target_list = synonym_list
                        break
                else:
                    target_list = [target_cell.value]
                    self.synonyms.append(target_list)
                old_list: list[str] = self.find_synonyms_for_value(
                    self.__dragged_item.value
                )
                target_list.extend(old_list)
                if old_list in self.synonyms:
                    self.synonyms.remove(old_list)
                self.__main_window.construct_attribute_table()
                event.accept()
                self.__main_window.add_state_to_history(copy.deepcopy(self.synonyms))
            self.__dragged_item = None
            self.setCursor(Qt.CursorShape.ArrowCursor)

        else:
            super().mouseReleaseEvent(event)
        self.clearSelection()
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Sets the cursor shape during a drag depending on the current mouse position.

        :param event: The triggering event
        """
        self.clearSelection()
        if self.__dragged_item != None:
            self.__updateMouseAndSelection(event)
        else:
            super().mouseMoveEvent(event)
        self.update()

    def __updateMouseAndSelection(self, event: QMouseEvent | QWheelEvent) -> None:
        self.clearSelection()
        if self.__dragged_item != None:
            if self.__can_drop(event.position().toPoint()):
                self.setCursor(Qt.CursorShape.DragCopyCursor)
                # target_cell: QTableWidgetItem = self.itemAt(event.position().toPoint())
            else:
                self.setCursor(Qt.CursorShape.ForbiddenCursor)
            self.__dragged_item.setSelected(True)
        self.update()

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Keeps dragged item selected."""
        super().wheelEvent(event)
        self.clearSelection()
        self.__updateMouseAndSelection(event)

    def __can_drop(self, point: QPoint) -> bool:
        """Returns whether a drop can currently happen at the given.

        :param point: The position where the drop would happen
        :return: True or False depending on whether a drop can happen
        """
        target_cell: QTableWidgetItem = self.itemAt(point)
        return (
            self.__dragged_item != None
            and target_cell is not None
            and isinstance(target_cell, MergeableAttributeItem)
            and target_cell.value != self.__dragged_item.value
            and self.column(target_cell) == self.column(self.__dragged_item)
        )

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

    def set_value(self, row: int, column: int, value: str, count: int) -> None:
        """Sets the item at a given row and column to a MergeableAttributeItem with given parameters

        :param row: The row to set the item in
        :param column: The column to set the item in
        :param value: The value for the MergeableAttributeItem
        :param count: The count for the MergeableAttributeItem
        """
        self.setItem(row, column, MergeableAttributeItem(value, count))
        self.values = []
