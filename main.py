import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Smart Room Planner")
        self.setGeometry(200, 100, 800, 600)

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        # File -> New
        new_action = QAction("New", self)
        file_menu.addAction(new_action)

        # File -> Exit
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
