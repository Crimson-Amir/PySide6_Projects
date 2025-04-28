import sys
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QListWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        listwidget = QListWidget()
        listwidget.addItems(["One", "Two", "Three"])

        listwidget.currentItemChanged.connect(self.index_changed)
        listwidget.currentTextChanged.connect(self.text_changed)

        self.setCentralWidget(listwidget)

    def index_changed(self, index):
        print(index.text())

    def text_changed(self, text):
        print(text)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
