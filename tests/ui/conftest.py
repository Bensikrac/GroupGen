import pytest
from PyQt6.QtWidgets import QApplication


@pytest.fixture(scope="session", autouse=True)
def app_fixture():
    app = QApplication([])
    yield app
    app.quit()
