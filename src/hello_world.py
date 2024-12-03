"""example code for a hello world with qt"""
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt


class HelloWindow(QMainWindow):
    """A basic hello-world example window"""

    def __init__(self):
        """Default initializer"""
        super().__init__()

        self.setWindowTitle("Hello World")
        label = QLabel("Hello World")
        label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.setCentralWidget(label)


if __name__ == "__main__":
    app = QApplication([])
    window = HelloWindow()
    window.show()

    app.exec()
