import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QWidget, 
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QGraphicsScene, QGraphicsView, 
    QGraphicsRectItem
)
from PyQt5.QtCore import Qt


class SmartRoomPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Room Planner")
        self.setGeometry(100, 100, 900, 600)

        self.scene = QGraphicsScene()
        self.canvas = QGraphicsView(self.scene)

        # Placeholder at start
        self.recent_label = QLabel("Recent work: none")
        self.main_layout = QHBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.recent_label)

        # Menu Bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        new_action = QAction("New", self)
        new_action.triggered.connect(self.show_new_project)
        file_menu.addAction(new_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def show_new_project(self):
        # Clear layout
        for i in reversed(range(self.main_layout.count())):
            widget_to_remove = self.main_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        # Input fields
        self.width_input = QLineEdit()
        self.height_input = QLineEdit()
        self.orientation_input = QComboBox()
        self.orientation_input.addItems(["North", "East", "South", "West"])

        self.generate_button = QPushButton("Generate Room")
        self.generate_button.clicked.connect(self.generate_room)

        # Input panel
        self.input_panel = QWidget()
        self.input_panel_layout = QVBoxLayout()
        self.input_panel.setLayout(self.input_panel_layout)

        self.input_panel_layout.addWidget(QLabel("Room Width:"))
        self.input_panel_layout.addWidget(self.width_input)

        self.input_panel_layout.addWidget(QLabel("Room Height:"))
        self.input_panel_layout.addWidget(self.height_input)

        self.input_panel_layout.addWidget(QLabel("Orientation:"))
        self.input_panel_layout.addWidget(self.orientation_input)

        self.input_panel_layout.addWidget(self.generate_button)

        # Add widgets to layout
        self.main_layout.addWidget(self.input_panel, 1)
        self.main_layout.addWidget(self.canvas, 3)

    def generate_room(self):
        self.scene.clear()

        try:
            width = float(self.width_input.text())
            height = float(self.height_input.text())
        except ValueError:
            self.scene.addText("Invalid input! Enter numbers.")
            return

        # Normalize scaling so rooms always fit
        max_dim = max(width, height)
        scale_factor = 300 / max_dim  # fit within ~300px

        rect_item = QGraphicsRectItem(0, 0, width * scale_factor, height * scale_factor)
        rect_item.setBrush(Qt.lightGray)
        self.scene.addItem(rect_item)

        # Add orientation label at bottom
        orientation = self.orientation_input.currentText()
        self.scene.addText(f"{int(width)} x {int(height)} | {orientation}").setPos(10, height * scale_factor + 10)

        # Center view on drawing
        self.canvas.setSceneRect(self.scene.itemsBoundingRect())
        self.canvas.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartRoomPlanner()
    window.show()
    sys.exit(app.exec_())
