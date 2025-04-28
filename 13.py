import sys
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QListWidget,
    QLineEdit,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.lineedit = QLineEdit()
        self.lineedit.setMaxLength(10)
        self.lineedit.setPlaceholderText("Enter your text")

        self.lineedit.returnPressed.connect(self.return_pressed)
        self.lineedit.selectionChanged.connect(self.selection_changed)
        self.lineedit.textChanged.connect(self.text_changed)
        self.lineedit.textEdited.connect(self.text_edited)
        self.lineedit.setInputMask('000.000.000.000;_')


        self.setCentralWidget(self.lineedit)

    def return_pressed(self):
        print("Return pressed!")
        self.lineedit.setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.lineedit.selectedText())

    def text_changed(self, text):
        print("Text changed...")
        print(text)

    def text_edited(self, text):
        print("Text edited...")
        print(text)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
