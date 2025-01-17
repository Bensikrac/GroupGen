"""Module containing tests for attribute_merge_table.py."""

import sys
from unittest.mock import patch
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QMouseEvent, QDrag, QDropEvent, QDragEnterEvent
from PyQt6.QtCore import Qt, QEvent, QPointF, QPoint, QMimeData

from app import MainWindow
from ui.attribute_merge_table import AttributeMergeTable, MergeableAttributeItem


def test_mouse_press_event():
    """Tests if a QMouseEvent correctly sets the dragged item."""
    app = QApplication.instance() or QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    test_table: AttributeMergeTable = test_window.attributes_table
    test_item = MergeableAttributeItem("test", 2)
    test_table.setItem(0, 0, test_item)
    test_event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPointF(20, 150),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    with patch.object(QDrag, "exec", return_value=None):
        with patch.object(AttributeMergeTable, "itemAt", return_value=test_item):
            test_table.mousePressEvent(test_event)
    assert test_table.dragged_item == test_item


def test_drop_event_new_synonym():
    """Tests if a QDropEvent is correctly handled if all synonyms that need to be created are new."""
    app = QApplication.instance() or QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    test_table: AttributeMergeTable = test_window.attributes_table
    drag_item = MergeableAttributeItem("lorem", 2)
    target_item = MergeableAttributeItem("ipsum", 3)
    test_table.synonyms = [["foo", "bar"]]
    test_table.setItem(0, 0, target_item)
    test_table.dragged_item = drag_item
    test_event = QDropEvent(
        QPointF(0, 0),
        Qt.DropAction.CopyAction,
        QMimeData(),
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
        QEvent.Type.Drop,
    )
    with (
        patch.object(AttributeMergeTable, "itemAt", return_value=target_item),
        patch.object(MainWindow, "print_attribute_table", return_value=None) as mock,
    ):
        test_table.dropEvent(test_event)
    assert test_table.dragged_item == None
    assert test_table.synonyms == [["foo", "bar"], ["ipsum", "lorem"]]
    mock.assert_called()


def test_drop_event_merge_synonym():
    """Tests if a QDropEvent is correctly handled if synonyms need to be merged."""
    app = QApplication.instance() or QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    test_table: AttributeMergeTable = test_window.attributes_table
    drag_item = MergeableAttributeItem("lorem", 2)
    target_item = MergeableAttributeItem("ipsum", 3)
    test_table.synonyms = [["lorem", "foo"], ["ipsum", "bar"]]
    test_table.setItem(0, 0, target_item)
    test_table.dragged_item = drag_item
    test_event = QDropEvent(
        QPointF(0, 0),
        Qt.DropAction.CopyAction,
        QMimeData(),
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
        QEvent.Type.Drop,
    )
    with (
        patch.object(AttributeMergeTable, "itemAt", return_value=target_item),
        patch.object(MainWindow, "print_attribute_table", return_value=None) as mock,
    ):
        test_table.dropEvent(test_event)
    assert test_table.dragged_item == None
    test_table.synonyms = [["ipsum", "bar", "lorem", "foo"]]
    mock.assert_called()


def test_find_preferred_synonym():
    """Tests if find_preferred_synonym returns correct values."""
    app = QApplication.instance() or QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    test_table: AttributeMergeTable = test_window.attributes_table
    test_table.synonyms = [["lorem", "foo"], ["ipsum", "bar"], ["a", "b", "c"]]
    assert test_table.find_preferred_synonym("foo") == "lorem"
    assert test_table.find_preferred_synonym("ipsum") == "ipsum"
    assert test_table.find_preferred_synonym("42") == "42"


def test_accept_events():
    """Tests if QDragMoveEvents are accepted without issue."""
    app = QApplication.instance() or QApplication(sys.argv)
    test_window: MainWindow = MainWindow("assets/main_window.ui")
    test_table: AttributeMergeTable = test_window.attributes_table
    test_enter_event = QDragEnterEvent(
        QPoint(0, 0),
        Qt.DropAction.CopyAction,
        QMimeData(),
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    test_table.dragEnterEvent(test_enter_event)
    test_table.dragMoveEvent(test_enter_event)
