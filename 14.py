import sys
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QListWidget,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        spinbox = QSpinBox()
        spinbox = QDoubleSpinBox()
        # spinbox.setMinimum(-10)
        # spinbox.setMaximum(3)
        spinbox.setRange(-10, 3)
        # Or: doublespinbox.setRange(-10, 3)

        spinbox.setPrefix("$")
        spinbox.setSuffix("c")
        spinbox.setSingleStep(.2)
        spinbox.lineEdit().setReadOnly(True)
        spinbox.valueChanged.connect(self.value_changed)
        spinbox.textChanged.connect(self.value_changed_str)

        self.setCentralWidget(spinbox)

    def value_changed(self, value):
        print(value)

    def value_changed_str(self, str_value):
        print(str_value)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
