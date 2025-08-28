import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QComboBox, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QAction
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt


class RoomPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Room Planner + Daylight Simulator (Prototype)")
        self.setGeometry(100, 100, 800, 600)

        self.room_item = None
        self.unit = 20.0

        # Menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        new_action = QAction("New", self)
        new_action.triggered.connect(self.show_main_ui)
        file_menu.addAction(new_action)

        # Start screen
        self.start_widget = QWidget()
        start_layout = QVBoxLayout()
        self.recent_label = QLabel("Recently closed: demo_project.json")
        start_layout.addWidget(self.recent_label)
        self.start_widget.setLayout(start_layout)
        self.setCentralWidget(self.start_widget)

    def show_main_ui(self):
        self.main_widget = QWidget()
        main_layout = QHBoxLayout()
        self.main_widget.setLayout(main_layout)

        # Left panel
        left_panel = QVBoxLayout()

        left_panel.addWidget(QLabel("Room Width (m):"))
        self.width_input = QLineEdit()
        left_panel.addWidget(self.width_input)

        left_panel.addWidget(QLabel("Room Height (m):"))
        self.height_input = QLineEdit()
        left_panel.addWidget(self.height_input)

        left_panel.addWidget(QLabel("Orientation:"))
        self.orientation_dropdown = QComboBox()
        self.orientation_dropdown.addItems(["North", "East", "South", "West"])
        left_panel.addWidget(self.orientation_dropdown)

        self.generate_button = QPushButton("Generate Room")
        self.generate_button.clicked.connect(self.generate_room)
        left_panel.addWidget(self.generate_button)

        # Furniture inputs
        left_panel.addWidget(QLabel("Furniture Type:"))
        self.furniture_dropdown = QComboBox()
        self.furniture_dropdown.addItems(["Bed", "Table", "Chair", "Wardrobe"])
        left_panel.addWidget(self.furniture_dropdown)

        left_panel.addWidget(QLabel("Furniture Width (m):"))
        self.furn_w_input = QLineEdit()
        left_panel.addWidget(self.furn_w_input)

        left_panel.addWidget(QLabel("Furniture Height (m):"))
        self.furn_h_input = QLineEdit()
        left_panel.addWidget(self.furn_h_input)

        self.add_furn_button = QPushButton("Add Furniture")
        self.add_furn_button.clicked.connect(self.add_furniture)
        left_panel.addWidget(self.add_furn_button)

        self.info_label = QLabel("Enter room info and generate.")
        left_panel.addWidget(self.info_label)

        # Canvas
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # Add layouts
        main_layout.addLayout(left_panel, 1)
        main_layout.addWidget(self.view, 3)

        self.setCentralWidget(self.main_widget)

    def generate_room(self):
        self.scene.clear()

        try:
            width = float(self.width_input.text())
            height = float(self.height_input.text())
            if width <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            self.info_label.setText("Enter valid positive numbers for width & height.")
            return

        orientation = self.orientation_dropdown.currentText()
        self.info_label.setText(f"{width} m × {height} m | {orientation}")

        max_display = 420.0
        max_dim = max(width, height)
        self.unit = max_display / max_dim if max_dim > 0 else 20.0
        self.unit = min(self.unit, 60.0)
        self.unit = max(self.unit, 6.0)

        rect_w = width * self.unit
        rect_h = height * self.unit
        self.offset_x, self.offset_y = 40, 40

        pen = QPen(Qt.black)
        brush = QBrush(Qt.lightGray)

        # store room rect as parent
        self.room_item = self.scene.addRect(0, 0, rect_w, rect_h, pen, brush)
        self.room_item.setPos(self.offset_x, self.offset_y)
        self.room_item.setTransformOriginPoint(rect_w / 2, rect_h / 2)

        rotation_map = {"North": 0, "East": 90, "South": 180, "West": 270}
        self.room_item.setRotation(rotation_map.get(orientation, 0))

        self.view.setSceneRect(self.scene.itemsBoundingRect())
        room_bounds = self.room_item.sceneBoundingRect()
        self.scene.addText(f"{width:.2f} m × {height:.2f} m  |  {orientation}") \
            .setPos(room_bounds.left(), room_bounds.bottom() + 8)

        padded = self.scene.itemsBoundingRect().adjusted(-20, -20, 20, 60)
        self.view.fitInView(padded, Qt.KeepAspectRatio)

    def add_furniture(self):
        if not hasattr(self, "room_item") or self.room_item is None:
            self.info_label.setText("Please generate a room first.")
            return

        try:
            f_w = float(self.furn_w_input.text())
            f_h = float(self.furn_h_input.text())
            if f_w <= 0 or f_h <= 0:
                raise ValueError
        except ValueError:
            self.info_label.setText("Enter valid positive numbers for furniture.")
            return

        furn_type = self.furniture_dropdown.currentText()

        colors = {
            "Bed": QColor(200, 100, 100),
            "Table": QColor(100, 150, 200),
            "Chair": QColor(100, 200, 120),
            "Wardrobe": QColor(180, 160, 90)
        }
        color = colors.get(furn_type, QColor(150, 150, 150))

        rect_w = f_w * self.unit
        rect_h = f_h * self.unit

        # add furniture as a CHILD of the room
        furn_item = QGraphicsRectItem(0, 0, rect_w, rect_h)
        furn_item.setBrush(QBrush(color))
        furn_item.setPen(QPen(Qt.black))
        furn_item.setToolTip(furn_type)

        # parent to room
        furn_item.setParentItem(self.room_item)

        # simple placement inside room (top-left corner for now)
        furn_item.setPos(10, 10)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoomPlanner()
    window.show()
    sys.exit(app.exec_())
