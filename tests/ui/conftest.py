import pytest
from PyQt6.QtWidgets import QApplication

from src.app import MainWindow


@pytest.fixture(scope="session", autouse=True)
def app_fixture():
    app = QApplication([])
    yield app
    app.quit()


@pytest.fixture(scope="session")
def main_window_fixture(app_fixture):
    window = MainWindow()
    # window.show()
    yield window
    window.close()
