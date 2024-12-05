from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from app_functionality import push_buttons


class MainWindow(QMainWindow):
    """Main Window class"""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("GroupGen")

        input_button: QPushButton = QPushButton("Neue Eingabe")
        input_button.clicked.connect(push_buttons.file_picker)

        self.setCentralWidget(input_button)


if __name__ == "__main__":
    app: QApplication = QApplication([])
    window: MainWindow = MainWindow()
    window.show()

    app.exec()
