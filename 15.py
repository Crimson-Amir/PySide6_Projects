import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QListWidget,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QSlider,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        slider = QSlider(Qt.Orientation.Horizontal)

        slider.setRange(-10, 10)
        slider.setValue(10)
        # Or: widget.setRange(-10,3)

        slider.setSingleStep(2)

        slider.valueChanged.connect(self.value_changed)
        slider.sliderMoved.connect(self.slider_position)
        slider.sliderPressed.connect(self.slider_pressed)
        slider.sliderReleased.connect(self.slider_released)

        self.setCentralWidget(slider)

    def value_changed(self, value):
        print(value)

    def slider_position(self, position):
        print("position", position)

    def slider_pressed(self):
        print("Pressed!")

    def slider_released(self):
        print("Released")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()