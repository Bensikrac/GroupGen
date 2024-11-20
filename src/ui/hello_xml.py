from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic


class DesignerHelloWindow(QMainWindow):
    """A basic hello-world example window loaded from an xml file"""

    def __init__(self):
        """Default initializer"""
        super().__init__()

        uic.loadUi(
            "hello_world.ui",  # relative to working directory, this may need to be done differently in the final program
            self,
        )


if __name__ == "__main__":
    app: QApplication = QApplication([])
    window: QMainWindow = DesignerHelloWindow()
    window.show()

    app.exec()
