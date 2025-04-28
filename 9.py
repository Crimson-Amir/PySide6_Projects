import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        label_1 = QLabel("QLineEdit")
        label_1.setText("Hello World!")
        font = label_1.font()
        font.setPointSize(20)
        label_1.setFont(font)
        label_1.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        self.setCentralWidget(label_1)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()