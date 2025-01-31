"""Module containing tests for attribute_merge_table.py."""

from unittest.mock import patch
from PyQt6.QtGui import QMouseEvent, QDrag, QDropEvent, QDragEnterEvent
from PyQt6.QtCore import Qt, QEvent, QPointF, QPoint, QMimeData

from app import MainWindow
from ui.attribute_merge_table import AttributeMergeTable, MergeableAttributeItem
from ui.attribute_table_items import CheckableHeaderItem


def test_mouse_press_event(main_window_fixture):
    """Tests if a left QMouseEvent correctly sets the dragged item and a right doesnt."""
    test_table: AttributeMergeTable = main_window_fixture.attributes_table
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


def test_drop_event_new_synonym(app_fixture):
    """Tests if a QDropEvent is correctly handled if all synonyms that need to be created are new."""
    test_window: MainWindow = MainWindow()
    test_table: AttributeMergeTable = test_window.attributes_table
    drag_item = MergeableAttributeItem("lorem", 2)
    target_item = MergeableAttributeItem("ipsum", 3)
    test_table.synonyms = [["foo", "bar"]]
    test_table.setItem(0, 0, target_item)
    test_table._AttributeMergeTable__dragged_item = drag_item
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
        patch.object(
            MainWindow, "construct_attribute_table", return_value=None
        ) as mock,
    ):
        test_table.dropEvent(test_event)
    assert test_table._AttributeMergeTable__dragged_item == None
    assert test_table.synonyms == [["foo", "bar"], ["ipsum", "lorem"]]
    mock.assert_called()
    test_window.close()


def test_drop_event_merge_synonym(app_fixture):
    """Tests if a QDropEvent is correctly handled if synonyms need to be merged."""
    test_window: MainWindow = MainWindow()
    test_table: AttributeMergeTable = test_window.attributes_table
    drag_item = MergeableAttributeItem("lorem", 2)
    target_item = MergeableAttributeItem("ipsum", 3)
    test_table.synonyms = [["lorem", "foo"], ["ipsum", "bar"]]
    test_table.setItem(0, 0, target_item)
    test_table._AttributeMergeTable__dragged_item = drag_item
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
        patch.object(
            MainWindow, "construct_attribute_table", return_value=None
        ) as mock,
    ):
        test_table.dropEvent(test_event)
    assert test_table._AttributeMergeTable__dragged_item == None
    test_table.synonyms = [["ipsum", "bar", "lorem", "foo"]]
    mock.assert_called()
    test_window.close()


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
