import sys
from PySide6.QtGui import QPixmap
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
    QWidget,
    QVBoxLayout,
    QSlider,
    QSpinBox,
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        label_1 = QLabel()
        label_1.setPixmap(QPixmap("otje.webp"))
        label_1.setScaledContents(True)
        check_box = QCheckBox("Check me")
        check_box.setCheckState(Qt.CheckState.Checked)
        check_box.setCheckState(Qt.CheckState.PartiallyChecked)
        check_box.stateChanged.connect(self.print_smt)
        layout = QVBoxLayout()
        layout.addWidget(label_1)
        layout.addWidget(check_box)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def print_smt(self, state):
        print(Qt.CheckState.Checked.value)
        print("CheckBox state changed:", state)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()