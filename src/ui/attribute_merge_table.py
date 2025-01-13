from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QApplication
from PyQt6.QtGui import QMouseEvent, QDrag
from PyQt6.QtCore import Qt, QMimeData, QPoint, QPointF


class MergeableAttributeItem(QTableWidgetItem):
    value: str

    def __init__(self, value: str, count):
        super().__init__(f"{value}: {count}")
        self.value = value


class AttributeMergeTable(QTableWidget):
    from app import MainWindow

    frequencies: list[(str, int)] = []
    synonyms: list[list[str]] = []
    values: list[list[str]] = []
    dragged_item: MergeableAttributeItem | None
    main_window: MainWindow

    def setMainWindow(self, main_window: MainWindow):
        self.main_window = main_window

    # def print_table(self):

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragged_item = self.itemAt(event.pos())

            drag: QDrag = QDrag(self)
            mime_data: QMimeData = QMimeData()
            drag.setMimeData(mime_data)
            drag.exec()

    def dropEvent(self, event):
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
        for synonym_list in self.synonyms:
            if value == synonym_list[0]:
                return synonym_list
        return [value]

    def find_preferred_synonym(self, value: str) -> str:
        for synonym_list in self.synonyms:
            if value in synonym_list:
                return synonym_list[0]
        return value

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def setValue(self, row: int, column: int, value: str, count: int) -> None:
        self.setItem(row, column, MergeableAttributeItem(value, count))
        self.values = []
