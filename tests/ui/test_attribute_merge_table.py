"""Module containing tests for attribute_merge_table.py."""

import time
from unittest.mock import patch
from PyQt6.QtGui import QMouseEvent, QWheelEvent
from PyQt6.QtCore import Qt, QEvent, QPointF, QPoint
from PyQt6.QtWidgets import QTableWidget

from app import MainWindow
from ui.attribute_merge_table import AttributeMergeTable, MergeableAttributeItem
from ui.attribute_table_items import CheckableHeaderItem


def test_mouse_press_event(app_fixture):
    """Tests if a left QMouseEvent correctly sets the dragged item and a right doesnt."""
    test_window: MainWindow = MainWindow()
    test_table: AttributeMergeTable = test_window.attributes_table
    test_item = MergeableAttributeItem("test", 2)
    test_table.setItem(0, 0, test_item)
    test_event_1 = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPointF(20, 150),
        Qt.MouseButton.RightButton,
        Qt.MouseButton.RightButton,
        Qt.KeyboardModifier.NoModifier,
    )

    with patch.object(AttributeMergeTable, "itemAt", return_value=test_item):
        test_table.mousePressEvent(test_event_1)
    assert test_table._AttributeMergeTable__dragged_item == None

    test_event_2 = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPointF(20, 150),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )

    with patch.object(AttributeMergeTable, "itemAt", return_value=test_item):
        test_table.mousePressEvent(test_event_2)
    assert test_table._AttributeMergeTable__dragged_item == test_item
    test_window.close()


def test_mouse_release_right(app_fixture):
    """Tests if releasing the right mouse is correctly handled."""
    test_window: MainWindow = MainWindow()
    test_table: AttributeMergeTable = test_window.attributes_table
    test_item: MergeableAttributeItem = MergeableAttributeItem("test", 2)
    test_table._AttributeMergeTable__dragged_item = test_item
    test_event: QMouseEvent = QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        QPointF(20, 150),
        Qt.MouseButton.RightButton,
        Qt.MouseButton.RightButton,
        Qt.KeyboardModifier.NoModifier,
    )
    with patch.object(QTableWidget, "mouseReleaseEvent", return_value=None) as mock:
        test_table.mouseReleaseEvent(test_event)
    mock.assert_called()


def test_drop_event_new_synonym(app_fixture):
    """Tests if a drop is correctly handled if all synonyms that need to be created are new."""
    test_window: MainWindow = MainWindow()
    test_table: AttributeMergeTable = test_window.attributes_table
    drag_item: MergeableAttributeItem = MergeableAttributeItem("lorem", 2)
    target_item: MergeableAttributeItem = MergeableAttributeItem("ipsum", 3)
    test_table.synonyms = [["foo", "bar"]]
    test_table.setItem(0, 0, target_item)
    test_table._AttributeMergeTable__dragged_item = drag_item
    test_event: QMouseEvent = QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        QPointF(20, 150),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    with (
        patch.object(AttributeMergeTable, "itemAt", return_value=target_item),
        patch.object(
            test_window, "construct_attribute_table", return_value=None
        ) as mock,
    ):
        test_table.mouseReleaseEvent(test_event)
    assert test_table._AttributeMergeTable__dragged_item == None
    assert test_table.synonyms == [["foo", "bar"], ["ipsum", "lorem"]]
    mock.assert_called()
    test_window.close()


def test_drop_event_merge_synonym(app_fixture):
    """Tests if a drop is correctly handled if synonyms need to be merged."""
    test_window: MainWindow = MainWindow()
    test_table: AttributeMergeTable = test_window.attributes_table
    drag_item: MergeableAttributeItem = MergeableAttributeItem("lorem", 2)
    target_item: MergeableAttributeItem = MergeableAttributeItem("ipsum", 3)
    test_table.synonyms = [["lorem", "foo"], ["ipsum", "bar"]]
    test_table.setItem(0, 0, target_item)
    test_table._AttributeMergeTable__dragged_item = drag_item
    test_event: QMouseEvent = QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        QPointF(20, 150),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    with (
        patch.object(AttributeMergeTable, "itemAt", return_value=target_item),
        patch.object(
            MainWindow, "construct_attribute_table", return_value=None
        ) as mock,
    ):
        test_table.mouseReleaseEvent(test_event)
    assert test_table._AttributeMergeTable__dragged_item == None
    test_table.synonyms = [["ipsum", "bar", "lorem", "foo"]]
    mock.assert_called()
    test_window.close()


def test_mouse_move(main_window_fixture):
    """Tests if the cursor shape is set correctly during drag and drop."""
    test_window: MainWindow = MainWindow()
    test_table: AttributeMergeTable = test_window.attributes_table
    drag_item: MergeableAttributeItem = MergeableAttributeItem("lorem", 2)
    target_item: MergeableAttributeItem = MergeableAttributeItem("ipsum", 3)
    test_table.setItem(0, 0, target_item)
    test_table.setItem(0, 1, drag_item)
    test_table._AttributeMergeTable__dragged_item = drag_item
    test_event: QMouseEvent = QMouseEvent(
        QEvent.Type.MouseMove,
        QPointF(20, 150),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    with patch.object(AttributeMergeTable, "itemAt", return_value=target_item):
        test_table.mouseMoveEvent(test_event)

    assert test_table.cursor().shape() == Qt.CursorShape.DragCopyCursor

    test_table.synonyms = []
    test_event_2: QMouseEvent = QMouseEvent(
        QEvent.Type.MouseMove,
        QPointF(20, 150),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    with patch.object(AttributeMergeTable, "itemAt", return_value=drag_item):
        test_table.mouseMoveEvent(test_event_2)

    assert test_table.cursor().shape() == Qt.CursorShape.ForbiddenCursor

    test_table.setCursor(Qt.CursorShape.ArrowCursor)
    test_table._AttributeMergeTable__dragged_item = None
    test_event_3: QMouseEvent = QMouseEvent(
        QEvent.Type.MouseMove,
        QPointF(20, 150),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    test_table.mouseMoveEvent(test_event_3)
    assert test_table.cursor().shape() == Qt.CursorShape.ArrowCursor

    test_window.close()


def test_wheel_event(app_fixture):
    test_window: MainWindow = MainWindow()
    test_table: AttributeMergeTable = test_window.attributes_table
    drag_item: MergeableAttributeItem = MergeableAttributeItem("lorem", 2)
    test_table._AttributeMergeTable__dragged_item = drag_item
    test_event: QWheelEvent = QWheelEvent(
        QPointF(20, 150),
        QPointF(20, 150),
        QPoint(0, 10),
        QPoint(0, 10),
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
        Qt.ScrollPhase.ScrollUpdate,
        False,
    )
    test_table.wheelEvent(test_event)
    assert test_table._AttributeMergeTable__dragged_item != None


def test_find_preferred_synonym(app_fixture):
    """Tests if find_preferred_synonym returns correct values."""
    test_window: MainWindow = MainWindow()
    test_table: AttributeMergeTable = test_window.attributes_table
    test_table.synonyms = [["lorem", "foo"], ["ipsum", "bar"], ["a", "b", "c"]]
    assert test_table.find_preferred_synonym("foo") == "lorem"
    assert test_table.find_preferred_synonym("ipsum") == "ipsum"
    assert test_table.find_preferred_synonym("42") == "42"
    test_window.close()


def test_header_clicked(app_fixture):
    """Tests if headers behave correctly when clicked."""
    test_window: MainWindow = MainWindow()
    test_table: AttributeMergeTable = test_window.attributes_table
    test_table.setColumnCount(2)
    test_item_1: CheckableHeaderItem = CheckableHeaderItem("lorem", True)
    test_item_2: CheckableHeaderItem = CheckableHeaderItem("ipsum", True)
    test_table.setHorizontalHeaderItem(0, test_item_1)
    test_table.setHorizontalHeaderItem(1, test_item_2)

    test_table._AttributeMergeTable__header_click(0)
    assert not test_item_1.checked
    assert test_item_1.font().strikeOut()

    test_table._AttributeMergeTable__header_click(0)
    assert test_item_1.checked
    assert not test_item_1.font().strikeOut()

    test_table._AttributeMergeTable__header_click(1)
    assert not test_item_2.checked
    assert test_item_2.font().strikeOut()

    test_window.close()
