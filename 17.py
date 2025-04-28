import sys
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        combobox = QComboBox()
        combobox.addItems(["One", "Two", "Three"])

        combobox.currentIndexChanged.connect(self.index_changed)

        combobox.currentTextChanged.connect(self.text_changed)
        combobox.setEditable(True)
        combobox.InsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        combobox.setMaxCount(5)

        self.setCentralWidget(combobox)


    def index_changed(self, index):
        print(index)

    def text_changed(self, text):
        print(text)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()