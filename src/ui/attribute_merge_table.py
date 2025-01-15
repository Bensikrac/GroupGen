"""Module containing the classes for the attribute frequency table and cells within that table."""

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QApplication
from PyQt6.QtGui import QMouseEvent, QDrag
from PyQt6.QtCore import Qt, QMimeData, QPoint, QPointF


class MergeableAttributeItem(QTableWidgetItem):
    """A QTableWidgetItem that stores its value while displaying the value with a count."""

    value: str

    def __init__(self, value: str, count):
        """Initializes the item with the given value and count

        :param value: The value for the item
        :param count: The count for the item
        """
        super().__init__(f"{value}: {count}")
        self.value = value


class AttributeMergeTable(QTableWidget):
    """A QtableWidtet to display attribute value frequencies that can be merged via drag and drop"""

    from app import MainWindow

    frequencies: list[(str, int)] = []
    synonyms: list[list[str]] = []
    values: list[list[str]] = []
    dragged_item: MergeableAttributeItem | None
    main_window: MainWindow

    def setMainWindow(self, main_window: MainWindow) -> None:
        """Sets the table's connected main window to a given value.

        :param main_window: The main window to set as this table's main window
        """
        self.main_window = main_window

    # def print_table(self):

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Starts a drag and saves the original dragged item.

        :param event: The triggering event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragged_item = self.itemAt(event.pos())

            drag: QDrag = QDrag(self)
            mime_data: QMimeData = QMimeData()
            drag.setMimeData(mime_data)
            drag.exec()

    def dropEvent(self, event) -> None:
        """Accepts the drop if it is valid cell and updates the synonyms and table accordingly

        :param event: The triggering event
        """
        target_cell: QTableWidgetItem = self.itemAt(event.position().toPoint())
        if (
            target_cell != None
            and isinstance(target_cell, MergeableAttributeItem)
            and target_cell.value != self.dragged_item.value
        ):
            found_list: bool = False
            target_list: list[str] | None = None
            for synonym_list in self.synonyms:
                if (
                    target_cell.value == synonym_list[0]
                    and not self.dragged_item.value in synonym_list
                ):
                    target_list = synonym_list
                    break
            if target_list == None:
                target_list = [target_cell.value]
                self.synonyms.append(target_list)
            old_list: list[str] = self.find_synonyms_for_value(self.dragged_item.value)
            target_list.extend(old_list)
            if old_list in self.synonyms:
                self.synonyms.remove(old_list)
            self.clearContents()
            self.main_window.print_attribute_table()
            event.accept()
            print(self.synonyms)
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

    def dragEnterEvent(self, event) -> None:
        """Accepts the triggering event.

        :param event: The triggering event
        """
        event.accept()

    def dragMoveEvent(self, event) -> None:
        """Accepts the triggering event.

        :param event: The triggering event
        """
        event.accept()

    def setValue(self, row: int, column: int, value: str, count: int) -> None:
        """Sets the item at a given row and column to a MergeableAttributeItem with given parameters

        :param row: The row to set the item in
        :param column: The column to set the item in
        :param value: The value for the MergeableAttributeItem
        :param count: The count for the MergeableAttributeItem
        """
        self.setItem(row, column, MergeableAttributeItem(value, count))
        self.values = []
